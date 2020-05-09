
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

# Startup example: 26657
# rly pth show kira-alpha_kira-1
# rly pth show kira-alpha_gameofzoneshub-1
# 
# console args
t0 = time.time()
SRC_JSON_DIR=sys.argv[1]
SRC_MNEMONIC=sys.argv[2]
DST_JSON_DIR=sys.argv[3]
DST_MNEMONIC=sys.argv[4]
BUCKET=sys.argv[5]
SHUTDOWN=sys.argv[6]
path=sys.argv[7]
key_prefix=sys.argv[8]
min_ttl=sys.argv[9]
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
state_file_txt = StateHelper.S3ReadText(BUCKET,state_file_path)
state_file = {}
if None == state_file_txt: # error
    raise Exception(f"Error occurred while fetching {state_file_path} from {BUCKET} bucket")
elif len(state_file_txt) > 10:
     state_file = json.loads(state_file_txt)

# this command is asserted and throws if connection is not estbalished
connection = IBCHelper.ConnectWithJson(SRC_JSON_DIR, SRC_MNEMONIC, DST_JSON_DIR, DST_MNEMONIC, BUCKET, path, key_prefix, timeout, min_ttl)


print(f"INFO: Fetching state file from S3...")
state_file_txt = StateHelper.S3ReadText(BUCKET,state_file_path)
old_connection_update = 0 # the last time node was connected or updated
old_state_upload = 0 # last time state file was updated
old_total_uptime = 0 # sum of the connection uptime
time_start = time.time()

if None == state_file_txt: # error when fetching state file
   print(f"ERROR: Failed to download state file or access s3")
   print(f"INFO: Script Failed (1)")
   exit(1)
elif None != state_file_txt and (not state_file_txt): # empty state file
    print(f"WARNING: State file was not present in s3")
    connection["last-update"] = 0
    connection["upload-time"] = time_start
    connection["total-uptime"] = 0
else: # status exists, extract state file from json
    print(f"SUCCESS: State file was loaded")
    print(state_file_txt)
    state_file = json.loads(state_file_txt)
    old_connection_update = state_file["last-update"]
    old_state_upload = state_file["upload-time"]
    old_total_uptime = state_file["total-uptime"]
    connection["total-uptime"]=old_total_uptime
    connection["last-update"]=old_connection_update
    connection["upload-time"]=old_state_upload
    print(f"INFO: Last connection update: {timedelta(seconds=(time.time() - old_connection_update))}")
    print(f"INFO: Last state upload: {timedelta(seconds=(time.time() - old_state_upload))}")

if not connected:
    print(f"ERROR: Failed to establish connection using {SRC_JSON_DIR} and {DST_JSON_DIR}")
    if f"{SHUTDOWN}" == "True":
        print(f"INFO: Connection will be permanently shutdown")
        IBCHelper.ShutdownConnection(connection)
    else:
        print(f"INFO: Connection will NOT be shutdown")

    elpased_connection_update = time.time() - old_connection_update
    if (update_period/2) <= elpased_connection_update:
        print(f"INFO: Updating client despite errors...")
        if not RelayerHelper.UpdateClientConnection(connection):
            print(f"WARNING: Failed to update clients")
        else:
            print(f"SUCCESS: Client was updated")
            connection["last-update"] = time.time()

    RelayerHelper.PushPendingTransactions(path)
    connection["upload-time"] = time_start
    StateHelper.S3WriteText(connection,BUCKET,state_file_path);
    print(f"INFO: Script Failed (2)")
    exit(2)

src_chain_info = connection["src"]
dst_chain_info = connection["dst"]
src_id = src_chain_info["chain-id"]
dst_id = dst_chain_info["chain-id"]
src_key = src_chain_info["key-name"]
dst_key = dst_chain_info["key-name"]
src_denom = src_chain_info["default-denom"]
dst_denom = dst_chain_info["default-denom"]

dT0=int(time.time() - t0) # time between start of the scrip and relayer beeing ready to update connection
print(f"SUCCESS: connection between {src_id} and {dst_id} was established within {timedelta(seconds=dT0)}, path: '{path}'")
print(f"INFO: Entering connection sustainably mode")

while True:
    if not IBCHelper.TestConnection(connection):
        connection["success"] = False
        break;
    elapsed = time.time() - time_start
    elpased_connection_update = time.time() - old_connection_update
    elapsed_state_upload = time.time() - old_state_upload

    total_uptime = old_total_uptime + elapsed
    connection["total-uptime"]=total_uptime
    print(f"_________________________________")
    print(f"| PATH: {path}")
    print(f"| TIME: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"|--------------------------------|")
    print(f"| INFO: Current Connection:      - {timedelta(seconds=elapsed)}")
    print(f"| INFO: Total uptime:            - {timedelta(seconds=total_uptime)}")
    print(f"| INFO: Next connection update:  - {max(0,int(update_period - elpased_connection_update))}s")
    print(f"| INFO: Next state update:       - {max(0,int(upload_period-elapsed_state_upload))}s")
    print(f"| INFO: Source Key balance:      - {src_key} {ClientHelper.QueryFeeTokenBalance(src_chain_info)} {src_denom}")
    print(f"| INFO: Destination Key balance: - {dst_key} {ClientHelper.QueryFeeTokenBalance(dst_chain_info)} {dst_denom}")
    print(f"|________________________________|")
    
    if update_period <= elpased_connection_update:
        print(f"INFO: Elapsed minmum trust period of {timedelta(seconds=update_period)}, updating client connection...")
        last_update=time.time() # time has to be measured before the function is called
        if RelayerHelper.UpdateClientConnection(connection):
            print(f"SUCCESS: Connection was updated!")
            connection["last-update"]=last_update
            old_connection_update=last_update
        else:
            print(f"ERROR: Failed to update connection :(")

        old_state_upload = time.time()
        connection["upload-time"] = old_state_upload
        if not StateHelper.TryS3WriteText(connection,BUCKET,state_file_path):
            print(f"ERROR: Failed to upload state file.")

    elif upload_period <= elapsed_state_upload:
        print(f"INFO: Elapsed minmum upload period of {timedelta(seconds=upload_period)}")
        old_state_upload = time.time()
        connection["upload-time"] = old_state_upload
        if not StateHelper.TryS3WriteText(connection,BUCKET,state_file_path):
            print(f"ERROR: Failed to upload state file.")

    print(f"INFO: Pushing any pending transactions...")
    RelayerHelper.PushPendingTransactions(path)
    IBCHelper.UpdateLiteClients(connection)

    time.sleep(float(30))

elapsed = time.time() - time_start
print(f"ERROR: Failed to maitain connection between {src_id} and {dst_id}, Uptime: {timedelta(seconds=elapsed)}")
connection["upload-time"] = time.time()
StateHelper.S3WriteText(connection,BUCKET,state_file_path)
print(f"INFO: Script Failed (3)")
exit(3)
