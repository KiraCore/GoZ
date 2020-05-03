
import IBCHelper
import RelayerHelper
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
from datetime import timedelta


# Startup example: 26657
# rly pth show kira-alpha_kira-1
# python3 $RELAY_SCRIPS/phase1.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $GOZCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $BUCKET False "test" "test_key" 5
# python3 $RELAY_SCRIPS/phase1.py $GOZCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $BUCKET False "conn1"
# python3 $RELAY_SCRIPS/phase1.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $GOZCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $BUCKET True
# python3 $RELAY_SCRIPS/phase1.py $GOZCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $BUCKET True
# rly pth show kira-alpha_gameofzoneshub-1
# python3 $RELAY_SCRIPS/phase1.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $HUBCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $BUCKET False "alpha_goz" "test_key"
# python3 $RELAY_SCRIPS/phase1.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $HUBCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $BUCKET False "alpha_goz" "test_key"

# Update: (rm $RELAY_SCRIPS/phase1.py || true) && nano $RELAY_SCRIPS/phase1.py 
 
# console args
SRC_JSON_DIR=sys.argv[1]
SRC_MNEMONIC=sys.argv[2]
DST_JSON_DIR=sys.argv[3]
DST_MNEMONIC=sys.argv[4]
BUCKET=sys.argv[5]
SHUTDOWN=sys.argv[6]
PATH=sys.argv[7]
KEY_PREFIX=sys.argv[8]
TRUST_UPDATE_PERIOD=sys.argv[9]
PATH = None if ((not PATH) or (len(PATH) <= 1)) else PATH
KEY_PREFIX = "chain_key" if ((not KEY_PREFIX) or (len(KEY_PREFIX) <= 1)) else KEY_PREFIX
   
# constants 
connect_timeout = 60
update_period = int(TRUST_UPDATE_PERIOD)*60
upload_period = 60*5

print(f" _________________________________")
print(f"|     STARTING RELAYER v0.0.1     |")
print(f"|---------------------------------|")
print(f"| INFO: Connection Path:          - {PATH}")
print(f"| INFO: Key Prefix:               - {KEY_PREFIX}")
print(f"| INFO: S3 Bucket:                - {BUCKET}")
print(f"| INFO: Source Chain File:        - {SRC_JSON_DIR}")
print(f"| INFO: Destination Chain File:   - {DST_JSON_DIR}")
print(f"| INFO: Connection Update Period: - {timedelta(seconds=update_period)}")
print(f"| INFO: State Upload Period:      - {timedelta(seconds=upload_period)}")
print(f"|_________________________________|")

connection = IBCHelper.ConnectWithJson(SRC_JSON_DIR, SRC_MNEMONIC, DST_JSON_DIR, DST_MNEMONIC, BUCKET, PATH, KEY_PREFIX, connect_timeout)
connection = {} if not connection else connection
path = None if (not connection) else connection.get("path", PATH)
prefix = None if (not connection) else connection.get("key-prefix", KEY_PREFIX)
connected = False if ((not connection) or (not path) or (not prefix)) else connection.get("success", False)
state_file_path = $"relayer/{path}/{prefix}/state.json"

state_file_txt = StateHelper.S3ReadText(BUCKET,state_file_path)
old_connection_update = 0 # the last time node was connected or updated
old_upload_time = 0 # last time state file was updated
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
    connection["upload-time"] = time_start
    StateHelper.S3WriteText(connection,BUCKET,state_file_path);
    print(f"INFO: Script Failed (2)")
    exit(2)

src_chain_info = connection["src"]
dst_chain_info = connection["dst"]
src_id = src_chain_info["chain-id"]
dst_id = dst_chain_info["chain-id"]

print(f"SUCCESS: connection between {src_id} and {dst_id} was established, path: '{path}'")
print(f"INFO: Entering connection sustainably mode")

while True:
    if not IBCHelper.TestConnection(connection):
        connection["success"] = False
        break;
    elapsed = time.time() - time_start
    elpased_update = time.time() - old_connection_update
    
    total_uptime = old_total_uptime + elapsed
    connection["total-uptime"]=total_uptime
    print(f"INFO: Current Connection: {timedelta(seconds=elapsed)}")
    print(f"INFO: Total uptime: {timedelta(seconds=total_uptime)}")
    print(f"INFO: Elapsed since last update: {timedelta(seconds=elpased_update)}")
    
    if update_period < elpased_update:
        print(f"INFO: Elapsed minmum trust period of {timedelta(seconds=update_period)}, updating client connection...")
        last_update=time.time() # time has to be measured before the function is called
        if RelayerHelper.UpdateClientConnection(connection):
            print(f"SUCCESS: Connection was updated!")
            connection["last-update"]=last_update
        else:
            print(f"ERROR: Failed to update connection :(")

        connection["upload-time"] = time.time()
        if not StateHelper.S3WriteText(connection,BUCKET,state_file_path):
            print(f"ERROR: Failed to upload state file.")
        else:
            old_state_upload = time_start

    elapsed_upload = time.time() - old_state_upload
    if elapsed_upload < upload_period:
        print(f"INFO: Elapsed minmum upload period of {timedelta(seconds=upload_period)}")
        connection["upload-time"] = time.time()
        if not StateHelper.S3WriteText(connection,BUCKET,state_file_path):
            print(f"ERROR: Failed to upload state file.")
        else:
            old_state_upload = time_start

    time.sleep(float(5))

elapsed = time.time() - time_start
print(f"ERROR: Failed to maitain connection between {src_id} and {dst_id}, Uptime: {timedelta(seconds=elapsed)}")
connection["upload-time"] = time.time()
StateHelper.S3WriteText(connection,BUCKET,state_file_path)
print(f"INFO: Script Failed (3)")
exit(3)
