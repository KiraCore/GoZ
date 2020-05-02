import RelayerHelper
import StringHelper
import ArrayHelper
import subprocess
import json
import statistics
import sys
import os
import os.path
import time
from joblib import Parallel, delayed


def ClaimTokensWithMnemonic(chain_info, mnemonic, bucket, timeout):
    chain_id = chain_info["chain-id"]
    chain_key = chain_info["key"]
    chain_info_path = chain_info["file-path"]
    key_name = f"chain_key_{chain_id}"
    s3_key_path = f"{chain_id}/key.json"
    tmp_file=f"/tmp/{chain_id}_key.json"
    retry = 3 # 3x
    delay = 5 # 5s

    if not RelayerHelper.QueryLiteClientHeader(chain_id):
        # cleanup
        RelayerHelper.DeleteLiteClient(chain_id) # rly lite delete kira-1
        RelayerHelper.DeleteKey(chain_id, key_name) # rly keys delete kira-1 chain_key_kira-1
        RelayerHelper.ChainDelete(chain_id) # rly chains delete kira-1
    
        if not RelayerHelper.AddChainFromFile(chain_info_path): # rly chains add -f $BASECHAIN_JSON_PATH
            print(f"Failed adding new chain from '{chain_info_path}' file :(")
            return chain_info
        
        if mnemonic: # restore old key
            RelayerHelper.RestoreKey(chain_id, key_name, mnemonic) # rly keys restore kira-alpha chain_key_kira-alpha "$RLYKEY_MNEMONIC"
        else: # add new key
            print(f"Saving new key '{chain_id}' '{key_name}' to '{tmp_file}'...")
            key = RelayerHelper.UpsertKey(chain_id, key_name)
            StringHelper.WriteToFile(key,tmp_file)
            RelayerHelper.callRawTrue(f"AWSHelper s3 upload-object --bucket='{bucket}' --path='{s3_key_path}' --input='{tmp_file}'",True)
    
        if not RelayerHelper.ConfigureDefaultKey(chain_id, key_name): # rly ch edit kira-alpha key chain_key_kira-alpha
            print(f"Failed to configure '{chain_id}' chain to use {key_name} key by default :(")
            return chain_info
    
        if not RelayerHelper.InitLiteClient_Process(chain_id, timeout, retry, delay): # rly lite init kira-alpha -f
            print(f"Failed lite client init of the '{chain_id}' chain :(")
            return chain_info
        else:
            print(f"SUCCESS: Lite client of the chain '{chain_id}' was initialized")
    else: # update
        if not RelayerHelper.UpdateLiteClient_Process(chain_id, timeout, retry, delay): 
            print(f"Failed updating lite client of the '{chain_id}' chain :(")
            return chain_info
        else: 
            print(f"SUCCESS: Lite client of the chain '{chain_id}' was updated")

    if not RelayerHelper.RequestTokens_Process(chain_id, timeout, retry, delay): # rly testnets request kira-1
        print(f"Faucet {chain_id} didn't gave out any tokens :(")

    chain_info["balance"]=RelayerHelper.QueryBalance(chain_id)
    chain_info["address"]=RelayerHelper.QueryChainAddress(chain_id)
    return chain_info

def ClaimTokensWithBucket(chain_info, bucket, timeout):
    chain_id = chain_info["chain-id"]
    chain_key = chain_info["key"]
    chain_info_path = chain_info["file-path"]
    s3_key_path = f"{chain_id}/key.json"
    tmp_file=f"/tmp/{chain_id}_key.json"
   
    key = RelayerHelper.DownloadKey(bucket, s3_key_path, tmp_file)
    mnemonic=key["mnemonic"]
    return ClaimTokensWithMnemonic(chain_info, mnemonic, bucket, timeout)


def ClaimTokens(chain_info_path, mnemonic, bucket, timeout):
    # load chain info: key, chain-id, rpc-addr, account-prefix, gas, gas-prices, default-denom, trusting-period
    chain_info = json.load(open(chain_info_path))
    chain_info["file-path"] = chain_info_path
    chain_info["balance"] = None
    chain_info["address"] = None
    if mnemonic:
        return ClaimTokensWithMnemonic(chain_info, mnemonic, bucket, timeout)
    elif bucket:
        return ClaimTokensWithBucket(chain_info, bucket, timeout)
    else:
        raise Exception(f"bucket or mnemonic was not specified, failed to claim tokens")