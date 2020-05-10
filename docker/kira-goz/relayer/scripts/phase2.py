
import IBCHelper
import RelayerHelper
import ClientHelper
import StateHelper
import StringHelper
import ArrayHelper
import subprocess
import json
import statistics
import sys
import os
import time
import asyncio
# import settings
from joblib import Parallel, delayed
from datetime import timedelta, datetime


# Update: (rm $SELF_SCRIPTS/phase2.py || true) && nano $SELF_SCRIPTS/phase2.py 

# console args
t0 = time.time()
SRC_JSON_DIR=sys.argv[1]
SRC_MNEMONIC=sys.argv[2]
DST_JSON_DIR=sys.argv[3]
DST_MNEMONIC=sys.argv[4]
BUCKET=sys.argv[5]
path=sys.argv[6]
key_prefix=sys.argv[7]
min_ttl=sys.argv[8]
path = "default_path" if ((not path) or (len(path) <= 1)) else path
key_prefix = "chain_key" if ((not key_prefix) or (len(key_prefix) <= 1)) else key_prefix
min_ttl = int(min_ttl)*60

# constants 
timeout = 60
upload_period = 5*60

# variables
state_file = {}
src = None ; dst = None
src_conn_id = None ; dst_conn_id =  None
src_chain_id = None ; dst_chain_id = None
src_denom = None ; dst_denom = None
src_key = None ; dst_key = None

print(f" _________________________________")
print(f"|     STARTING RELAYER v0.0.2     |")
print(f"|---------------------------------|")
print(f"| INFO: Connection path:          - {path}")
print(f"| INFO: Key Prefix:               - {key_prefix}")
print(f"| INFO: S3 Bucket:                - {BUCKET}")
print(f"| INFO: Source Chain File:        - {SRC_JSON_DIR}")
print(f"| INFO: Destination Chain File:   - {DST_JSON_DIR}")
print(f"| INFO: Minimum Time To Live:     - {timedelta(seconds=min_ttl)}")
print(f"| INFO: State Upload Period:      - {timedelta(seconds=upload_period)}")
print(f"|_________________________________|")

state_file_path = f"relayer/{path}/{key_prefix}/state.json"
print(f"INFO: Fetching '{state_file_path}' state file from S3...")
state_file_txt = StateHelper.S3ReadText(BUCKET,state_file_path)
if None == state_file_txt: # error
    raise Exception(f"Error occurred while fetching {state_file_path} from {BUCKET} bucket")
elif len(state_file_txt) > 10:
     state_file = json.loads(state_file_txt)

# this command is asserted and throws if connection is not estbalished
connection = IBCHelper.ConnectWithJson(SRC_JSON_DIR, SRC_MNEMONIC, DST_JSON_DIR, DST_MNEMONIC, BUCKET, path, key_prefix, timeout, min_ttl)
time_start = time.time()
init_time = int(time_start - t0)

src = connection["src"]
dst = connection["dst"]
src_conn_id=connection["path-info"]["chains"]["src"]["connection-id"]
dst_conn_id=connection["path-info"]["chains"]["dst"]["connection-id"]
src_chain_id = src["chain-id"]
dst_chain_id = dst["chain-id"];
src_denom = src["default-denom"]
dst_denom = dst["default-denom"]
src_key = src["key-name"]
dst_key = dst["key-name"]

connection["init-time"] = init_time
connection["max-init-time"] = max_init_time = max(state_file.get("max-init-time", init_time), init_time)
connection["min-init-time"] = min_init_time = min(state_file.get("min-init-time", init_time), init_time)
upload_time = connection["upload-time"] = state_file.get("upload-time", 0) # time when state_info was uploaded for the last time
total_uptime = connection["total-uptime"] = state_file.get("total-uptime", 0)
total_transactions = connection["total-transactions"] = state_file.get("total-transactions", 0)
loop_start = time_start

print(f"INFO: Connection was established within {init_time}s")
print(f"INFO: Max init time: {max_init_time}s")
print(f"INFO: Min init time: {min_init_time}s")

gas_min = min(src.get("gas-min", 0),dst.get("gas-min", 0))
gas = 0
gas_max = max(src.get("gas-max", 1000000),dst.get("gas-max", 1000000))
gas_min_pass = gas_max
gas_adjustments = 0
failed_tx_counter = 0

while True:
    loop_elapsed = int(time.time() - loop_start)
    upload_elapsed = int(time.time() - upload_time)
    time_to_upload = int(upload_period - upload_elapsed)
    total_uptime = connection["total-uptime"] =  total_uptime + loop_elapsed
    loop_start = time.time()
    current_session = time.time() - time_start

    if failed_tx_counter > 10:
        print(f"FAILURE: More than 10 transactions failed in the row")
        break

    if not IBCHelper.TestConnection(connection):
        print(f"FAILURE: Connection was dropped or failed to query status. Current session duration: {timedelta(seconds=current_session)}")
        break

    ttl = RelayerHelper.GetRemainingTimesToLive(connection)

    if not ttl:
        print(f"FAILURE: Could not fetch remaining TTL")
        break

    ttl_src = int(ttl["src"]) # source connection time to live
    ttl_dst = int(ttl["dst"]) # destination connection time to live

    connection["src"] = src = ClientHelper.AssertRefreshBalances(src)
    connection["dst"] = dst = ClientHelper.AssertRefreshBalances(dst)
    src_balances = src["balance"] 
    dst_balances = dst["balance"]
    src_tokens = RelayerHelper.GetAmountByDenom(src_balances, src_denom)
    dst_tokens = RelayerHelper.GetAmountByDenom(dst_balances, dst_denom)
    src_cfg = RelayerHelper.ShowChain(src_chain_id) # rly ch show kira-alpha -j
    dst_cfg = RelayerHelper.ShowChain(dst_chain_id) # rly ch show kira-1 -j
    src_gas = src_cfg.get("gas", gas_min)
    dst_gas = dst_cfg.get("gas", gas_min)
    src_gas_price = float(src_cfg["gas-prices"][:-len(src_denom)])
    dst_gas_price = float(dst_cfg["gas-prices"][:-len(dst_denom)])
    src_fee = (src_gas * src_gas_price) + 1 # can't be 0
    dst_fee = (dst_gas * dst_gas_price) + 1 # can't be 0
    gas_now = max(src_gas, dst_gas)
    gas = gas_now if gas <= 0 else gas
    tps = (total_transactions/(total_uptime + 0.1))
    src_tx_left = src_tokens / src_fee
    dst_tx_left = dst_tokens / dst_fee
    max_transactions_left = min(src_tx_left, dst_tx_left)

    print(f"_________________________________")
    print(f"|        Source Chain            - {src_chain_id} ({src_conn_id})")
    print(f"|      Destination Chain         - {dst_chain_id} ({dst_conn_id})")
    print(f"|       Connection Path          - {path}")
    print(f"|        Date Time Now           - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"|--------------------------------|")
    print(f"| INFO: Current Session:         - {timedelta(seconds=current_session)}") # time since routine was started
    print(f"| INFO: Total uptime:            - {timedelta(seconds=total_uptime)}")
    print(f"| INFO: Source Client TTL:       - {max(0, ttl_src)}s")
    print(f"| INFO: Destination Client TTL:  - {max(0, ttl_dst)}s")
    print(f"| INFO: Next State Upload:       - {max(0,int(time_to_upload))}s")
    print(f"| INFO: Source Key balance:      - {src_key} {src_tokens} {src_denom}")
    print(f"| INFO: Destination Key balance: - {dst_key} {dst_tokens} {dst_denom}")
    print(f"| INFO: Total Transactions:      - {total_transactions}")
    print(f"| INFO: Max Transactions Left:   - {max_transactions_left}")
    print(f"| INFO: Average TPS:             - {tps}")
    print(f"| INFO: Gas Current:             - {gas_now}")
    print(f"| INFO: Gas Minimum:             - {gas_min}")
    print(f"|________________________________|")

########################################################################################################################################
#                                                          Tx Relay                                                                    #
########################################################################################################################################

    print(f"INFO: Starting transfer loop...")
    while min(ttl_src, ttl_dst) > min_ttl and time_to_upload > 0:
        tx_start = time.time()
        upload_elapsed = int(time.time() - upload_time)
        time_to_upload = int(upload_period - upload_elapsed)
        success=True
        amount_src = f"1{src_denom}"
        amount_dst = f"1{dst_denom}"
        tx_src = RelayerHelper.TransferTokensInternally(src, dst, amount_src, path)
        tx_dst = RelayerHelper.TransferTokensInternally(dst, src, amount_dst, path)
        if tx_src:
            print(f"INFO: Transfer {amount_src} from {src_chain_id} -> {dst_chain_id}, Result: {tx_src}")
        else:
            success = False
        if tx_dst:
            print(f"INFO: Transfer {amount_dst} from {dst_chain_id} -> {src_chain_id}, Result: {tx_dst}")
        else:
            success = False

        pending = RelayerHelper.CountPendingTransactions(path)
        if pending > 0:
            print(f"WARNING: Found {pending} pending transactions")
            
            if pending > 10:
                print(f"FATAL: Maximum number of pending transactions exceeded, shutting down connection")
                IBCHelper.ShutdownConnection(connection)
                exit(1)

            old_gas = gas
            gas = int(gas + ((gas_max - gas) / 2))
            IBCHelper.GasUpdateAssert(connection, gas)
            if not RelayerHelper.PushPendingTransactions(path):
                failed_tx_counter = failed_tx_counter + 1
                print(f"WARNING: Failed to push pending transactions ({failed_tx_counter})")
                break
            else:
                failed_tx_counter = 0
                gas = int(old_gas + (old_gas / 2))
                IBCHelper.GasUpdateAssert(connection, gas)
                continue
        elif success: # success and nothing is pending
            failed_tx_counter = 0
            gas_adjustments = gas_adjustments + 1
            gas_min_pass = gas if gas_min_pass > gas else gas_min_pass
            if gas_adjustments == 25: # change min gas after 25 successful transactions
                gas_min = gas_min_pass

            gas = int(gas - ((gas - gas_min) / 2))
            IBCHelper.GasUpdateAssert(connection, gas)

            tx_elapsed = float(time.time() - tx_start)
            ttl_src = int(ttl_src - tx_elapsed)
            ttl_dst = int(ttl_src - tx_elapsed)
            total_transactions = total_transactions + 2
            print(f"INFO: Current Tx Speed: {(2/tx_elapsed)} TPS, TTL: {min(ttl_src,ttl_dst)}s")
        else: # failure
            failed_tx_counter = failed_tx_counter + 1
            gas = int(gas + ((gas_max - gas) / 2))
            IBCHelper.GasUpdateAssert(connection, gas)
            print(f"ERROR: One of the transactions failed ({failed_tx_counter})")
            break

########################################################################################################################################

    skip_upload = False
    if ttl_src <= min_ttl:
        print(f"INFO: Remaining time to live of the source connection ({ttl_src}) is smaller than min TTL of {min_ttl}, updating...")
        if not RelayerHelper.UpdateClientConnection(src, path):
            print(f"WARNING: Failed to update source connection")
            skip_upload = True
        else:
            print(f"SUCCESS: Source client connection ({src_chain_id}) was updated")

    if ttl_dst <= min_ttl:
        print(f"INFO: Remaining time to live of the destination connection ({ttl_dst}) is smaller than min TTL of {min_ttl}, updating...")
        if not RelayerHelper.UpdateClientConnection(dst, path):
            print(f"WARNING: Failed to update destination connection")
            skip_upload = True
        else:
            print(f"SUCCESS: Destination client connection ({dst_chain_id}) was updated")

    print(f"INFO: Updating lite clients...");
    if not IBCHelper.RestartLiteClients(connection):
        print(f"WARNING: Failed to update lite clients")

    print(f"INFO: Pushing any pending transactions...");
    if not RelayerHelper.PushPendingTransactions(path):
        print(f"WARNING: Failed to push pending transactions")

    if time_to_upload < 0:
        connection["total-transactions"] = total_transactions
        connection["upload-time"] = upload_time = time.time()
        StateHelper.S3WriteText(connection,BUCKET,state_file_path);


print(f"ERROR: Failed to maitain connection between {src_id} and {dst_id}, Uptime: {timedelta(seconds=int(time.time() - time_start))}")
print(f"INFO: Script Failed (1)")
exit(1)
