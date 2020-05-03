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

# Update: (rm $RELAY_SCRIPS/ClientHelper.py || true) && nano $RELAY_SCRIPS/ClientHelper.py 
# rm $HOME/.relayer/config/config.yaml
def ShutdownClient(chain_info):
    chain_id = chain_info["chain-id"]
    key_name = chain_info["key-name"]
    RelayerHelper.DeleteKey(chain_id, key_name) # rly keys delete kira-alpha prefix_kira-alpha
    RelayerHelper.DeleteLiteClient(chain_id) # rly lite delete kira-alpha
    RelayerHelper.ChainDelete(chain_id) # rly chains delete kira-alpha

def InitializeClientWithMnemonic(chain_info, mnemonic, timeout):
    chain_id = chain_info["chain-id"]
    chain_info_path = chain_info["file-path"]
    key_name = chain_info["key-name"]
    bucket = chain_info["bucket"]
    s3_key_path = chain_info["s3-path"]
    tmp_file=chain_info["tmp-path"]

    retry = 3 # 3x
    delay = 5 # 5s

    def UpdateKeyIfNotSetAndConfigure():
        if not RelayerHelper.KeyExists(chain_id, key_name):
            print(f"WARNING: Key {key_name} of the {chain_id} chain does not exist, restoring...")
            if mnemonic: # restore old key
                RelayerHelper.RestoreKey(chain_id, key_name, mnemonic) # rly keys restore kira-alpha prefix_kira-alpha "$RLYKEY_MNEMONIC"
            else: # add new key
                print(f"Saving new key '{chain_id}' '{key_name}' to '{tmp_file}'...")
                key = RelayerHelper.UpsertKey(chain_id, key_name)
                StringHelper.WriteToFile(key,tmp_file)
                RelayerHelper.callRawTrue(f"AWSHelper s3 upload-object --bucket='{bucket}' --path='{s3_key_path}' --input='{tmp_file}'",True)

            if not RelayerHelper.KeyExists(chain_id, key_name):
                print(f"ERROR: Failed to restore key {key_name} of the chain {chain_id}")
            else:
                print(f"SUCCESS: Key {key_name} of the chain {chain_id} was restored")
        else:
            print(f"INFO: Key {key_name} of the {chain_id} already exists.")
        
        if not RelayerHelper.IsKeyConfigured(chain_id):
            if not RelayerHelper.ConfigureDefaultKey(chain_id, key_name): # rly ch edit kira-alpha key prefix_kira-alpha
                print(f"WARNING: Failed to configure chain {chain_id} to use {key_name} key by default")
            else:
                print(f"SUCCESS: Key {key_name} was configured as default of the chain {chain_id}")

    if not RelayerHelper.QueryLiteClientHeader(chain_id): # rly lite header kira-alpha
        if not RelayerHelper.UpsertChainFromFile(chain_info_path): # rly chains add -f $TESTCHAIN_JSON_PATH
            print(f"ERROR: Failed adding new chain from '{chain_info_path}' file :(")
            return chain_info

        print(f"SUCCESS: Chain {chain_id} was added from file {chain_info_path}")
        UpdateKeyIfNotSetAndConfigure()

        if not RelayerHelper.InitLiteClient_Process(chain_id, timeout, retry, delay): # rly lite init kira-alpha -f
            print(f"ERROR: Failed lite client init of the '{chain_id}' chain :(")
            return chain_info

        print(f"SUCCESS: Lite client of the chain '{chain_id}' was initialized")
    else: # update
        print(f"SUCCESS: Lite client header of the chain '{chain_id}' was found")
        UpdateKeyIfNotSetAndConfigure()

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

def InitializeClientWithBucket(chain_info, timeout):
    chain_id = chain_info["chain-id"]
    chain_info_path = chain_info["file-path"]
    bucket = chain_info["bucket"]
    key_name = chain_info["key-name"]
    s3_key_path = chain_info["s3-path"]
    tmp_file=chain_info["tmp-path"]
    
    key = RelayerHelper.DownloadKey(bucket, s3_key_path, tmp_file)
    mnemonic=key["mnemonic"]
    return InitializeClientWithMnemonic(chain_info, mnemonic, timeout)

def InitializeClient(chain_info, key_prefix, mnemonic, timeout):
    chain_info["balance"] = None
    chain_info["address"] = None

    key_prefix = "chain_key" if not key_prefix else key_prefix
    chain_id = chain_info["chain-id"]
    key_name = f"{key_prefix}_{chain_id}"

    chain_info["key-prefix"] = key_prefix
    chain_info["key-name"] = key_name
    chain_info["s3-path"] = f"{chain_id}/{key_name}.json"
    chain_info["tmp-path"] = "/tmp/{chain_id}_{key_name}.json"

    if mnemonic:
        return InitializeClientWithMnemonic(chain_info, mnemonic, timeout)
    elif bucket:
        return InitializeClientWithBucket(chain_info, timeout)
    else:
        raise Exception(f"bucket or mnemonic was not specified, failed to initialize client")

def InitializeClientWithJsonFile(json_path, key_prefix, mnemonic, bucket, timeout):
    chain_info = json.load(open(json_path))
    chain_info["file-path"] = json_path
    chain_info["bucket"] = bucket
    return InitializeClient(chain_info, key_prefix, mnemonic, timeout)

def QueryFeeTokenBalance(chain_info):
    chain_id = chain_info["chain-id"]
    denom = chain_info["default-denom"]

    if not denom:
        print(f"WARNING: Chain {chain_id} does not have a default denom for the fee token defined")
        return 0

    address = chain_info["address"]
    balances=RelayerHelper.TryQueryBalance(chain_id)
    return RelayerHelper.GetAmountByDenom(balances, denom)



