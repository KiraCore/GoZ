
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
DESTINATION_RLYS_DIR=sys.argv[1]

# env variables
RLYKEY_MNEMONIC = os.getenv('RLYKEY_MNEMONIC')
BASECHAIN_JSON_PATH = os.getenv('BASECHAIN_JSON_PATH')
BUCKET = os.getenv('BUCKET')

base_chain_info = FaucetHelper.ClaimTokens(BASECHAIN_JSON_PATH, RLYKEY_MNEMONIC, BUCKET)
ext_chains_info = {}

# interate all config files
for filename in os.listdir(DESTINATION_RLYS_DIR):
    
    file_dir=f"{DESTINATION_RLYS_DIR}/{filename}"
    print(f"Loading... {file_dir}")

    ext_chain_info = FaucetHelper.ClaimTokens(file_dir,None,BUCKET)
    ext_chain_id = ext_chain_info["chain-id"]
    ext_chains_info[f"{ext_chain_id}"]=ext_chain_info

