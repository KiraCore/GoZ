import RelayerHelper
import StringHelper
import ArrayHelper
import StateHelper
import subprocess
import json
import statistics
import sys
import os
import os.path
import time
from joblib import Parallel, delayed

# Update: (rm $SELF_SCRIPTS/ClientHelper.py || true) && nano $SELF_SCRIPTS/ClientHelper.py 
# rm $HOME/.relayer/config/config.yaml
def ShutdownClient(chain_info):
    chain_id = chain_info["chain-id"]
    key_name = chain_info["key-name"]
    RelayerHelper.DeleteKey(chain_id, key_name) # rly keys delete kira-alpha prefix_kira-alpha
    RelayerHelper.DeleteLiteClient(chain_id) # rly lite delete kira-alpha
    RelayerHelper.ChainDelete(chain_id) # rly chains delete kira-alpha

# NOTE: Keys / chain's can be fully re-initalized without impacting client connection, this method can be used even during live operations / post initalization to update the rly
def InitializeClientWithMnemonic(chain_info, mnemonic):
    print(f"INFO: Initializing client with mnemonic...")
    chain_id = chain_info["chain-id"]
    chain_info_path = chain_info["file-path"]
    key_name = chain_info["key-name"]
    bucket = chain_info["bucket"]
    s3_key_path = chain_info["s3-path"]

    if not mnemonic:
        raise Exception(f"Failed to recover key {key_name}. Mnemonic was not defined.");

    if not RelayerHelper.UpsertChainFromFile(chain_info_path): # rly chains add -f $TESTCHAIN_JSON_PATH
        raise Exception(f"Failed adding new chain from '{chain_info_path}' file :(")

    if not RelayerHelper.KeyExists(chain_id, key_name):
        print(f"WARNING: Key {key_name} of the {chain_id} chain does not exist, restoring...")
        RelayerHelper.RestoreKey(chain_id, key_name, mnemonic) # rly keys restore $s k$s "$RLYKEY_MNEMONIC"

        if not RelayerHelper.KeyExists(chain_id, key_name):
            raise Exception(f"Failed to restore key {key_name} of the chain {chain_id}")

        print(f"SUCCESS: Key {key_name} of the chain {chain_id} was restored")
    else:
        print(f"INFO: Key {key_name} of the {chain_id} already exists")
    
    if not RelayerHelper.ConfigureDefaultKey(chain_id, key_name): # rly ch edit kira-alpha key prefix_kira-alpha
        raise Exception(f"Failed to configure chain {chain_id} to use {key_name} key by default")
    print(f"SUCCESS: Key {key_name} was configured as default of the chain {chain_id}")

    chain_info["address"] = address = RelayerHelper.QueryChainAddress(chain_id)

    if not address:
        raise Exception(f"Failed to query {chain_id} chain address")

    chain_info["address"] = str(chain_info["address"],"utf-8")

    if not StateHelper.TryS3FileExists(bucket, s3_key_path):
        print(f"INFO: Relayer key {key_name} was not present in S3, uploading...")
        key = { "mnemonic":mnemonic, "address":address } 
        StateHelper.S3WriteText(key, bucket, s3_key_path) # will throw if fails to upload

    chain_info["balance"] = balance = RelayerHelper.TryQueryBalance(chain_id)

    if (not balance) or (len(balance) <= 0):
        print(f"WARNING: Address {address} on the chain {chain_id} has no tokens deposited or query failed to fetch balance!")
        chain_info["balance"] = balance = None

    return chain_info

def InitializeClientWithBucket(chain_info):
    print(f"INFO: Initializing client with bucket...")
    return InitializeClientWithMnemonic(chain_info, StateHelper.DownloadKey(chain_info["bucket"], chain_info["s3-path"])["mnemonic"])

def InitializeClient(chain_info, key_prefix, mnemonic):
    chain_info["balance"] = None
    chain_info["address"] = None

    key_prefix = "chain_key" if not key_prefix else key_prefix
    chain_id = chain_info["chain-id"]
    key_name = f"{key_prefix}_{chain_id}"

    chain_info["key-prefix"] = key_prefix
    chain_info["key-name"] = key_name
    chain_info["s3-path"] = f"{chain_id}/{key_name}.json"

    if mnemonic:
        return InitializeClientWithMnemonic(chain_info, mnemonic)
    elif None != chain_info.Get("bucket", None):
        return InitializeClientWithBucket(chain_info)
    else:
        raise Exception(f"FATAL! Bucket or mnemonic was not specified, failed to initialize client.")

def QueryFeeTokenBalance(chain_info):
    chain_id = chain_info["chain-id"]
    denom = chain_info.get("default-denom")
    if not denom:
        print(f"WARNING: Chain {chain_id} does not have a default denom for the fee token defined")
        return 0
    balances=RelayerHelper.TryQueryBalance(chain_id)
    return RelayerHelper.GetAmountByDenom(balances, denom)

def AssertRefreshBalances(chain_info):
    chain_id = chain_info["chain-id"]
    denom = chain_info["default-denom"]
    address = chain_info.get("address","undefined")
    chain_info["balance"] = balances = RelayerHelper.TryQueryBalance(chain_id)
    if RelayerHelper.GetAmountByDenom(balances, denom) <= 0:
        raise Exception(f"Insufficient {denom} balance of the account '{chain_id}:{address}', client will not be able to further continue the connections unless {denom} tokens are available.")
    return chain_info

def InitializeClientWithJsonFile(json_path, key_prefix, mnemonic, bucket):
    print(f"INFO: Initializing IBC client with JSON file: {json_path}")
    chain_info = json.load(open(json_path))
    chain_info["file-path"] = json_path
    chain_info["bucket"] = bucket
    chain_info = InitializeClient(chain_info, key_prefix, mnemonic)
    chain_id = chain_info["chain-id"]
    denom = chain_info["default-denom"]
    address = chain_info.get("address","undefined")

    print(f"INFO: Requesting {denom} tokens from {chain_id} faucet...")
    if not RelayerHelper.TryRequestTokens(chain_id):
        print(f"WARNING: Failed to request {denom} tokens from the {chain_id} faucet...")
    chain_info = AssertRefreshBalances(chain_info)
    return chain_info
