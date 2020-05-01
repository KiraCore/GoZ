
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


# Startup example: 26657
# python3 $RELAY_SCRIPS/phase1.py "$BASECHAIN_JSON_PATH" "$RLYKEY_MNEMONIC" "$GOZCHAIN_JSON_PATH" "$RLYKEY_MNEMONIC"

# console args
SRC_JSON_DIR=sys.argv[1]
SRC_MNEMONIC=sys.argv[2]
DST_JSON_DIR=sys.argv[3]
DST_MNEMONIC=sys.argv[4]

# env variables
BUCKET = os.getenv('BUCKET')

# constants 
connect_timeout = 60

connection = IBCHelper.ConnectWithJson(SRC_JSON_DIR, SRC_MNEMONIC, DST_JSON_DIR, DST_MNEMONIC, BUCKET, connect_timeout)
connected = False if (not connection) else connection["success"]
path = None if (not connection) else connection["path"]

if (not connected):
   print(f"Failed to establish connection using {SRC_JSON_DIR} and {DST_JSON_DIR}")

src_chain_info = connection["src"]
dst_chain_info = connection["dst"]
src_id = src_chain_info["chain-id"]
dst_id = dst_chain_info["chain-id"]
src_balance = src_chain_info["balance"]
dst_balance = src_chain_info["balance"]

print(f"Success connection between {src_id} and {dst_id} was established, path: '{path}'")

