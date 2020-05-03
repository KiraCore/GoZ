
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
# python3 $RELAY_SCRIPS/phase1.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $GOZCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $BUCKET False "test" "test_key"
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
PATH = None if ((not PATH) or (len(PATH) <= 1)) else PATH
KEY_PREFIX = "chain_key" if ((not KEY_PREFIX) or (len(KEY_PREFIX) <= 1)) else KEY_PREFIX
   



# constants 
connect_timeout = 60

connection = IBCHelper.ConnectWithJson(SRC_JSON_DIR, SRC_MNEMONIC, DST_JSON_DIR, DST_MNEMONIC, BUCKET, PATH, KEY_PREFIX, connect_timeout)
connection = {} if not connection else connection
path = None if (not connection) else connection.get("path", PATH)
prefix = None if (not connection) else connection.get("key-prefix", KEY_PREFIX)
connected = False if ((not connection) or (not path) or (not prefix)) else connection.get("success", False)
state_file = $"relayer/{path}/{prefix}/state.json"

state_file_txt = StateHelper.S3ReadText(BUCKET,state_file)
state_file = {}
old_last_update = 0 # the last time node was connected or updated
old_upload_time = 0 # last time state file was updated
time_start = time.time()

if None == state_file_txt:
   print(f"ERROR: Failed to download state file or access s3")
   print(f"INFO: Script Failed (1)")
   exit(1)
elif None != state_file_txt and (not state_file_txt):
    print(f"WARNING: State file was not present in s3")
    connection["last-update"] = 0
    connection["upload-time"] = time_start
    StateHelper.S3WriteText(connection,BUCKET,state_file);
else:
    state_file = json.loads(state_file_txt)
    old_last_update = state_file["last-update"]
    old_upload_time = state_file["upload-time"]
    connection["last-update"]=old_last_update
    print(f"INFO: Last successfull update: {timedelta(seconds=(time.time() - old_last_update))}")
    print(f"INFO: Last state upload: {timedelta(seconds=(time.time() - old_upload_time))}")

if not connected:
    print(f"ERROR: Failed to establish connection using {SRC_JSON_DIR} and {DST_JSON_DIR}")
    if f"{SHUTDOWN}" == "True":
        print(f"INFO: Connection will be permanently shutdown")
        IBCHelper.ShutdownConnection(connection)
    else:
        print(f"INFO: Connection will NOT be shutdown")
    state_file["upload-time"] = time_start
    StateHelper.S3WriteText(connection,BUCKET,state_file);
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
        break;
    elapsed = time.time() - time_start
    print(f"INFO: Connection duration: {timedelta(seconds=elapsed)}")
    time.sleep(float(5))

    # UpdateClientConnection

elapsed = time.time() - time_start
print(f"ERROR: Failed to maitain connection between {src_id} and {dst_id}, Uptime: {timedelta(seconds=elapsed)}")
print(f"INFO: Script Failed (3)")
exit(3)

#if(len(src_balance) <= 0) and (len(src_balance) < 0)

#RelayerHelper.TransferTokens(src_chain_id, dst_chain_id, amount, dst_chain_addr)

# rly pth delete kira-alpha_hashquarkchain
    # rly pth gen kira-alpha transfer hashquarkchain transfer kira-alpha_hashquarkchain
    # rly transact link kira-alpha_kira-1
    # rly transact clients kira-alpha_kira-1 --debug # clients connect
    # rly transact connection kira-alpha_kira-1 --debug # clients connection
    # rly transact channel kira-alpha_kira-1 --debug # channel connect

# rly pth delete kira-alpha_hashquarkchain
# rly pth gen kira-alpha transfer hashquarkchain transfer kira-alpha_hashquarkchain
# rly transact link kira-alpha_hashquarkchain --debug
# rly transact clients kira-alpha_hashquarkchain --debug # clients connect
# rly transact connection kira-alpha_hashquarkchain --debug # clients connection
# rly transact channel kira-alpha_hashquarkchain --debug # channel connect


# rly pth delete kira-alpha_hashquarkchain
# rly pth gen kira-alpha transfer hashquarkchain transfer kira-alpha_hashquarkchain
# rly transact clients kira-alpha_hashquarkchain --debug # clients connect
# rly transact connection kira-alpha_hashquarkchain --debug # clients connection
# rly transact channel kira-alpha_hashquarkchain --debug # channel connect
# rly transact link kira-alpha_hashquarkchain --debug

# rly transact channel-close kira-alpha_hashquarkchain
# rly tx channel-close kira-alpha_hashquarkchain --timeout 10s



#status = None if (not path_info) else path_info["status"]
#connected = None if (not status) else (status["chains"] and status["clients"] and status["connection"] and status["channel"])


# rly transact connection kira-alpha_kava-ibc
# rly pth show kira-alpha_kava-ibc

# rly transact channel-close kira-alpha_nibiru-ibc
# rly pth delete kira-alpha_nibiru-ibc
# rly pth gen kira-alpha transfer nibiru-ibc transfer kira-alpha_nibiru-ibc
# rly transact link kira-alpha_nibiru-ibc --debug
# rly transact channel kira-alpha_nibiru-ibc --debug 



######################################### rly paths add kira-1 hashquarkchain kira-1_hashquarkchain
### rly pth gen kira-1 transfer hashquarkchain transfer kira-1_hashquarkchain
## rly tx link kira-1_hashquarkchain
#
## rly q bal kira-1 -j
## rly q bal hashquarkchain -j
#
##rly ch addr hashquarkchain
#
## rly tx transfer hashquarkchain kira-1 1quark true $(rly ch addr kira-1)
## rly tx transfer kira-1 hashquarkchain 1ukex true $(rly ch addr hashquarkchain)