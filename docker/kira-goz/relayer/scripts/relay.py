
import IBCHelper
import RelayerHelper
import FaucetHelper
import StringHelper
import ArrayHelper
import subprocess
import json
import statistics
import sys
import os
import time
from joblib import Parallel, delayed

# console args
SOURCE_JSON_PATH=sys.argv[1]
SRC_MNEMONIC=sys.argv[2]
DESTINATION_RLYS_DIR=sys.argv[3]
DST_MNEMONIC=sys.argv[4]
BUCKET=sys.argv[5]

# constants
connect_timeout = 60

# Startup Example:
# python3 $RELAY_SCRIPS/relay.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $RLYS_HOME "$RLYKEY_MNEMONIC" $BUCKET

for filename in os.listdir(DESTINATION_RLYS_DIR):
    src_json_dir = SOURCE_JSON_PATH
    dst_json_dir = f"{DESTINATION_RLYS_DIR}/{filename}"

    connection = IBCHelper.ConnectWithJson(src_json_dir, SRC_MNEMONIC, dst_json_dir, DST_MNEMONIC, BUCKET, connect_timeout)
    connected = False if (not connection) else connection["success"]
    path = None if (not connection) else connection["path"]
    
    if (not connected):
       print(f"Failed to establish connection using {src_json_dir} and {dst_json_dir}.")
       continue

    src_chain_info = connection["src"]
    dst_chain_info = connection["dst"]
    src_id = src_chain_info["chain-id"]
    dst_id = dst_chain_info["chain-id"]
    
    print(f"SUCCESS: Connection between {src_id} and {dst_id} was established, path: '{path}'")

    IBCHelper.TransferEachToken(src_chain_info, dst_chain_info, path, 2)
    IBCHelper.TransferEachToken(dst_chain_info, src_chain_info, path, 1)

