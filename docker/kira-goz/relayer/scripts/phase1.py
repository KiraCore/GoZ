
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
state_file_txt = StateHelper.S3ReadText(BUCKET,state_file_path)
state_file = {}
if None == state_file_txt: # error
    raise Exception(f"Error occurred while fetching {state_file_path} from {BUCKET} bucket")
elif len(state_file_txt) > 10:
     state_file = json.loads(state_file_txt)

# this command is asserted and throws if connection is not estbalished
connection = IBCHelper.ConnectWithJson(SRC_JSON_DIR, SRC_MNEMONIC, DST_JSON_DIR, DST_MNEMONIC, BUCKET, path, key_prefix, timeout, min_ttl)
time_start = time.time()
init_time = int(time_start - t0)

src = connection["src"];
dst = connection["dst"];
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
loop_start = time_start

print(f"INFO: Connection was established within {init_time}s")
print(f"INFO: Max init time: {max_init_time}s")
print(f"INFO: Min init time: {min_init_time}s")

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

    ttl = RelayerHelper.GetRemainingTimeToLive(connection)
    ttl_src = int(ttl["src"]) # source connection time to live
    ttl_dst = int(ttl["dst"]) # destination connection time to live
    ttl_min = int(ttl["min"]) # minimum time to live

    print(f"_________________________________")
    print(f"| SRC: {src_chain_id}")
    print(f"| DST: {dst_chain_id}")
    print(f"| PATH: {path}")
    print(f"| TIME: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"|--------------------------------|")
    print(f"| INFO: Current Session:         - {timedelta(seconds=current_session)}") # time since routine was started
    print(f"| INFO: Total uptime:            - {timedelta(seconds=total_uptime)}")
    print(f"| INFO: Remaining Time To Live:  - {max(0, ttl_min)}s")
    print(f"| INFO: Next State Upload:       - {max(0,int(time_to_upload))}s")
    print(f"| INFO: Source Key balance:      - {src_key} {ClientHelper.QueryFeeTokenBalance(src)} {src_denom}")
    print(f"| INFO: Destination Key balance: - {dst_key} {ClientHelper.QueryFeeTokenBalance(dst)} {dst_denom}")
    print(f"|________________________________|")

    skip_upload = False
    if ttl_src <= min_ttl:
        print(f"INFO: Remaining time to live of the source connection ({ttl_src}) is smaller than min TTL of {min_ttl}, updating...")
        if not RelayerHelper.UpdateClientConnection(src, path):
            print(f"WARNING: Failed to update source connection")
            skip_upload = True

    if ttl_dst <= min_ttl:
        print(f"INFO: Remaining time to live of the destination connection ({ttl_dst}) is smaller than min TTL of {min_ttl}, updating...")
        if not RelayerHelper.UpdateClientConnection(dst, path):
            print(f"WARNING: Failed to update destination connection")
            skip_upload = True
            
    if skip_upload:
        continue
    
    if time_to_upload < 0:
        connection["upload-time"] = upload_time = time.time()
        StateHelper.S3WriteText(connection,BUCKET,state_file_path);

    print(f"INFO: Pushing any pending transactions...")
    if not RelayerHelper.PushPendingTransactions(path):
        print(f"WARNING: Failed to push pending transactions")



# loop exited


print(f"ERROR: Failed to maitain connection between {src_id} and {dst_id}, Uptime: {timedelta(seconds=int(time.time() - time_start))}")
print(f"INFO: Script Failed (1)")
exit(1)
