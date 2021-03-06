
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
from joblib import Parallel, delayed
from datetime import timedelta, datetime

# Update: (rm $SELF_SCRIPTS/phase1.py || true) && nano $SELF_SCRIPTS/phase1.py 

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
upload_period = 2*60

print(f" _________________________________")
print(f"|     STARTING RELAYER v0.0.1     |")
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
state_file = StateHelper.S3ReadJson(BUCKET,state_file_path)
if None == state_file: # error
    raise Exception(f"Error occurred while fetching {state_file_path} from {BUCKET} bucket")

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
connection["max-init-time"] = max_init_time = state_file.get("max-init-time", init_time)
connection["min-init-time"] = min_init_time = state_file.get("min-init-time", init_time)
upload_time = connection["upload-time"] = state_file.get("upload-time", 0) # time when state_info was uploaded for the last time
total_uptime = connection["total-uptime"] = state_file.get("total-uptime", 0)
loop_start = time_start

src_gas_min = src.get("gas-min", 50000)
dst_gas_min = dst.get("gas-min", 50000)
src_gas_max = src.get("gas-max", src_gas_min)
dst_gas_max = dst.get("gas-max", src_gas_min)
src_cfg = RelayerHelper.ShowChain(src_chain_id) # rly ch show kira-alpha -j
dst_cfg = RelayerHelper.ShowChain(dst_chain_id) # rly ch show kira-1 -j
src_gas_default = src_cfg.get("gas", src_gas_min)
dst_gas_default = dst_cfg.get("gas", dst_gas_min)

print(f"INFO: Connection was established within {init_time}s")
print(f"INFO: Max init time: {max_init_time}s")
print(f"INFO: Min init time: {min_init_time}s")
print(f"INFO: SRC => Gas Min ({src_gas_min}), Gas Now ({src_gas_default}), Gas Max ({src_gas_max})")
print(f"INFO: DST => Gas Min ({dst_gas_min}), Gas Now ({dst_gas_default}), Gas Max ({dst_gas_max})")

while True:
    loop_elapsed = int(time.time() - loop_start)
    upload_elapsed = int(time.time() - upload_time)
    time_to_upload = int(upload_period - upload_elapsed)
    total_uptime = connection["total-uptime"] =  total_uptime + loop_elapsed
    loop_start = time.time()
    current_session = time.time() - time_start

    if not IBCHelper.TestConnection(connection):
        print(f"FAILURE: Connection was dropped or failed to query status. Current session duration: {timedelta(seconds=current_session)}")
        break

    ttl = RelayerHelper.GetRemainingTimesToLive(connection)

    if not ttl:
        print(f"FAILURE: Could not fetch remaining TTL")
        break

    ttl_src = int(ttl["src"]) # source connection time to live
    ttl_dst = int(ttl["dst"]) # destination connection time to live

    src_cfg = RelayerHelper.ShowChain(src_chain_id)
    dst_cfg = RelayerHelper.ShowChain(dst_chain_id)
    src_gas = src_cfg["gas"]
    dst_gas = dst_cfg["gas"]

    connection["src"] = src = ClientHelper.AssertRefreshBalances(src)
    connection["dst"] = dst = ClientHelper.AssertRefreshBalances(dst)
    src_gas_price = float(src_cfg["gas-prices"][:-len(src_denom)])
    dst_gas_price = float(dst_cfg["gas-prices"][:-len(dst_denom)])
    src_tokens = RelayerHelper.GetAmountByDenom(src["balance"], src_denom)
    dst_tokens = RelayerHelper.GetAmountByDenom(dst["balance"], dst_denom)
    src_fee = int(src_gas * src_gas_price)
    dst_fee = int(dst_gas * dst_gas_price)
    src_tx_left = int(src_tokens / (src_fee + 1))
    dst_tx_left = int(dst_tokens / (dst_fee + 1))

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
    print(f"| INFO: Source Key balance:      - {src_key} {ClientHelper.QueryFeeTokenBalance(src)} {src_denom}")
    print(f"| INFO: Destination Key balance: - {dst_key} {ClientHelper.QueryFeeTokenBalance(dst)} {dst_denom}")
    print(f"| INFO: Source Chain GAS:        - {src_gas}\t| {src_gas_price} {src_denom}")
    print(f"| INFO: Destination Chain GAS:   - {dst_gas}\t| {dst_gas_price} {dst_denom}")
    print(f"| INFO: Source Tx Fee:           - {src_fee} {src_denom}")
    print(f"| INFO: Destination Tx Fee:      - {dst_fee} {dst_denom}")
    print(f"| INFO: Source Tx Left:          - {src_tx_left}")
    print(f"| INFO: Destination Tx Left:     - {dst_tx_left}")
    print(f"|________________________________|")
    skip_upload = False

    if ttl_src <= min_ttl:
        print(f"INFO: Setting GAS prices, to the minimum of SRC => {src_gas_min}")
        ClientHelper.GasUpdateAssert(src, src_gas_min)
        print(f"INFO: Remaining time to live of the source connection ({ttl_src}) is smaller than min TTL of {min_ttl}, updating...")
        if not RelayerHelper.UpdateClientConnection(src, path): # rly transact raw update-client $s $d $(rly pth s $p -j | jq -r '.chains.dst."client-id"')
            print(f"WARNING: Failed to update source connection")
            skip_upload = True
        else:
            print(f"SUCCESS: Source client connection ({src_chain_id}) was updated")

    if ttl_dst <= min_ttl:
        print(f"INFO: Setting GAS prices, to the minimum of DST => {dst_gas_min}")
        ClientHelper.GasUpdateAssert(dst, dst_gas_min)
        print(f"INFO: Remaining time to live of the destination connection ({ttl_dst}) is smaller than min TTL of {min_ttl}, updating...")
        if not RelayerHelper.UpdateClientConnection(dst, path):
            print(f"WARNING: Failed to update destination connection")
            skip_upload = True
        else:
            print(f"SUCCESS: Destination client connection ({dst_chain_id}) was updated")
            
    if skip_upload:
        continue
    
    print(f"INFO: Pushing any pending transactions...");
    if not RelayerHelper.PushPendingTransactions(path):
        print(f"WARNING: Failed to push pending transactions")

    print(f"INFO: Updating lite clients...");
    if not IBCHelper.RestartLiteClients(connection):
        print(f"WARNING: Failed to update lite clients")

    if time_to_upload < 0:
        connection["upload-time"] = upload_time = time.time()
        StateHelper.S3WriteText(connection,BUCKET,state_file_path);
    
    time.sleep(15)


print(f"ERROR: Failed to maitain connection between {src_id} and {dst_id}, Uptime: {timedelta(seconds=int(time.time() - time_start))}")
print(f"INFO: Script Failed (1)")
exit(1)
