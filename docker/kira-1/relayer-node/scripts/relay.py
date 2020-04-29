
import RelayerHelper
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

def ClaimFaucetTokens(chain_info_path, mnemonic):
    # load chain info: key, chain-id, rpc-addr, account-prefix, gas, gas-prices, default-denom, trusting-period
    chain_info = json.load(open(chain_info_path))
    chain_id = chain_info["chain-id"]
    chain_key = chain_info["key"]
    key_name = f"chain_key_{chain_id}"
    s3_key_path = f"{chain_id}/key.json"

    out1=RelayerHelper.callRaw(f"rly ch a -f {chain_info_path}",True)
    if not out1:
        print("Failed adding new chain")

    out2=RelayerHelper.callRawTrue(f"rly lite init {chain_id} -f",True)
    if not out2:
        print(f"Failed lite client init")

    key_exists=RelayerHelper.callRawTrue(f"AWSHelper s3 object-exists --bucket='{BUCKET}' --path='{s3_key_path}' --throw-if-not-found=true",False)
    tmp_file=f"/tmp/{chain_id}_key.json"
    if key_exists:
        if not mnemonic:
            RelayerHelper.callRawTrue(f"AWSHelper s3 download-object --bucket='{BUCKET}' --path='{s3_key_path}' --output={tmp_file}",True)
            mnemonic = json.load(open(tmp_file))["mnemonic"]
        key_exists = RelayerHelper.callRawTrue(f"rly keys restore '{chain_id}' '{key_name}' '{mnemonic}'",True) #restore key
    else:
        key_json=RelayerHelper.callRawTrue(f"rly keys add '{chain_id}' '{key_name}'",True)
        file = open(tmp_file, "w") 
        file.write(key_json) 
        file.close() 
        RelayerHelper.callRawTrue(f"AWSHelper s3 upload-object --bucket='{BUCKET}' --path='{s3_key_path}' --input={tmp_file}",True)
    
    out4=RelayerHelper.callRawTrue(f"rly testnets request {chain_id}",True)
    if not out4:
        print(f"Faucet didn't gave out any tokens :(")
    
    balance=RelayerHelper.callRawTrue(f"rly q bal {chain_id} -j",True)
    if not balance:
        print(f"Failed to get the balance")
        return chain_info
    else: 
        print(f"Got balance: ")
        print(balance)
        chain_info["balance"] = balance
        return chain_info

base_chain_info = ClaimFaucetTokens(BASECHAIN_JSON_PATH, RLYKEY_MNEMONIC)
ext_chains_info = {}

# interate all config files
for filename in os.listdir(DESTINATION_RLYS_DIR):
    
    file_dir=f"{DESTINATION_RLYS_DIR}/{filename}"
    print(f"Loading... {file_dir}")

    ext_chain_info = ClaimFaucetTokens(file_dir,None)
    ext_chain_id = ext_chain_info["chain-id"]
    ext_chains_info[f"{ext_chain_id}"]=ext_chain_info

