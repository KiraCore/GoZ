import RelayerHelper
import FaucetHelper
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

def ShutdownClient(chain_info):
    chain_id = chain_info["chain-id"]
    key_name = f"chain_key_{chain_id}"
    RelayerHelper.DeleteLiteClient(chain_id) # rly lite delete kira-1
    RelayerHelper.DeleteKey(chain_id, key_name) # rly keys delete kira-1 chain_key_kira-1
    RelayerHelper.ChainDelete(chain_id) # rly chains delete kira-1

def InitializeClientWithMnemonic(chain_info, mnemonic, bucket, timeout):
    chain_id = chain_info["chain-id"]
    chain_info_path = chain_info["file-path"]
    key_name = f"chain_key_{chain_id}"
    s3_key_path = f"{chain_id}/key.json"
    tmp_file=f"/tmp/{chain_id}_key.json"
    retry = 3 # 3x
    delay = 5 # 5s

    # rly chains show gameofzoneshub-1 
    if not RelayerHelper.QueryLiteClientHeader(chain_id):
        if not RelayerHelper.AddChainFromFile(chain_info_path): # rly chains add -f $BASECHAIN_JSON_PATH
            print(f"Failed adding new chain from '{chain_info_path}' file :(")
            return chain_info
        print(f"SUCCESS: Chain {chain_id} was added from file {chain_info_path}")
        
        if not RelayerHelper.KeyExists(chain_id, key_name):
            if mnemonic: # restore old key
                RelayerHelper.RestoreKey(chain_id, key_name, mnemonic) # rly keys restore kira-alpha chain_key_kira-alpha "$RLYKEY_MNEMONIC"
            else: # add new key
                print(f"Saving new key '{chain_id}' '{key_name}' to '{tmp_file}'...")
                key = RelayerHelper.UpsertKey(chain_id, key_name)
                StringHelper.WriteToFile(key,tmp_file)
                RelayerHelper.callRawTrue(f"AWSHelper s3 upload-object --bucket='{bucket}' --path='{s3_key_path}' --input='{tmp_file}'",True)
            print(f"SUCCESS: Key {key_name} was added to chain {chain_id}")
    
        if not RelayerHelper.ConfigureDefaultKey(chain_id, key_name): # rly ch edit kira-alpha key chain_key_kira-alpha
            print(f"WARNING: Failed to configure chain {chain_id} to use {key_name} key by default")

        if not RelayerHelper.InitLiteClient_Process(chain_id, timeout, retry, delay): # rly lite init kira-alpha -f
            print(f"ERROR: Failed lite client init of the '{chain_id}' chain :(")
            return chain_info
        print(f"SUCCESS: Lite client of the chain '{chain_id}' was initialized")
    else: # update
        if not RelayerHelper.UpdateLiteClient_Process(chain_id, timeout, retry, delay): 
            print(f"ERROR: Failed updating lite client of the '{chain_id}' chain :(")
            return chain_info
        print(f"SUCCESS: Lite client of the chain '{chain_id}' was updated")

    address = RelayerHelper.QueryChainAddress(chain_id)

    if not address:
        print(f"ERROR: Failed to query {chain_id} chain address")
        return chain_info

    balance = RelayerHelper.TryQueryBalance(chain_id)

    if (not balance) or (len(balance) <= 0):
        print(f"WARNING: Address {address} on the chain {chain_id} has no tokens deposited!")
        balance = None

    chain_info["address"] = address
    chain_info["balance"] = balance
    return chain_info

def InitializeClientWithBucket(chain_info, bucket, timeout):
    chain_id = chain_info["chain-id"]
    chain_info_path = chain_info["file-path"]
    s3_key_path = f"{chain_id}/key.json"
    tmp_file=f"/tmp/{chain_id}_key.json"
    key = RelayerHelper.DownloadKey(bucket, s3_key_path, tmp_file)
    mnemonic=key["mnemonic"]
    return InitializeClientWithMnemonic(chain_info, mnemonic, bucket, timeout)

def InitializeClient(chain_info, mnemonic, bucket, timeout):
    chain_info["balance"] = None
    chain_info["address"] = None
    if mnemonic:
        return InitializeClientWithMnemonic(chain_info, mnemonic, bucket, timeout)
    elif bucket:
        return InitializeClientWithBucket(chain_info, bucket, timeout)
    else:
        raise Exception(f"bucket or mnemonic was not specified, failed to initialize client")

def InitializeClientWithJsonFile(json_path, mnemonic, bucket, timeout):
    chain_info = json.load(open(json_path))
    chain_info["file-path"] = json_path
    return InitializeClient(chain_info, mnemonic, bucket, timeout)


def QueryFeeTokenBalance(chain_info):
    chain_id = chain_info["chain-id"]
    denom = chain_info["default-denom"]

    if not denom:
        print(f"WARNING: Chain {chain_id} does not have a default denom for the fee token defined")
        return 0

    address = chain_info["address"]
    balances=RelayerHelper.TryQueryBalance(chain_id)
    return RelayerHelper.GetAmountByDenom(balances, denom)



