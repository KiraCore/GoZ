
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
DESTINATION_RLYS_DIR=sys.argv[1]

# env variables
RLYKEY_MNEMONIC = os.getenv('RLYKEY_MNEMONIC')
BASECHAIN_JSON_PATH = os.getenv('BASECHAIN_JSON_PATH')
BUCKET = os.getenv('BUCKET')

base_chain_info = FaucetHelper.ClaimTokens(BASECHAIN_JSON_PATH, RLYKEY_MNEMONIC, BUCKET)
base_chain_id = base_chain_info["chain-id"]

if not base_chain_info["balance"]:
    print(f"Failed to acquire balance information from the base chain {base_chain_id}, aborting...")
    exit(1)

ext_chains_info = {}

# interate all config files
for filename in os.listdir(DESTINATION_RLYS_DIR):
    file_dir=f"{DESTINATION_RLYS_DIR}/{filename}"
    print(f"Loading... {file_dir}")

    # use diffrent key for each chain
    # ext_chain_info = FaucetHelper.ClaimTokens(file_dir,None,BUCKET)
    # use same key for each chain
    ext_chain_info = FaucetHelper.ClaimTokens(file_dir,RLYKEY_MNEMONIC,BUCKET)
    if not ext_chain_info:
        continue

    balance = ext_chain_info["balance"]
    denom = ext_chain_info["default-denom"]
    amount = RelayerHelper.GetAmountByDenom(balance, denom)
    if amount > 0:
       ext_chain_id = ext_chain_info["chain-id"]
       ext_chains_info[f"{ext_chain_id}"]=ext_chain_info

connections={}
for chain_id in ext_chains_info:
    chain_info=ext_chains_info[f"{chain_id}"]
    print(f"Connecting {base_chain_id} and {chain_id}...")
    connection=IBCHelper.Connect(base_chain_info, chain_info)
    if (not connection["success"]):
        print(f"Failed to connect {base_chain_id} and {chain_id}, info:")
        print(connection["info"])
        continue

    path=connection["path"]
    connections[f"{path}"]=connection
    print(f"SUCCESS!!! connected {base_chain_id} and {chain_id}")

    src = connection["src"]
    dst = connection["dst"]
    src_id = src["chain-id"]
    dst_id = dst["chain-id"]
    src_addr = src["address"]
    dst_addr = src["address"]
    src_balances = RelayerHelper.QueryBalance(src_id)
    dst_balances = RelayerHelper.QueryBalance(dst_id)
    
    print(f"Sending tokens from {src_id} to {dst_id}...")
    print(src_balances)
    print(dst_balances)
    for balance in src_balances:
        denom=balance["denom"]
        amount=int(balance["amount"])
        if amount <= 3:
            continue
        if not RelayerHelper.TransferTokens(src_id,dst_id,f"2{denom}",dst_addr):
            print(f"Failed to send 2{denom} from {src_id} to {dst_id}.")
        
    src_balances = RelayerHelper.QueryBalance(src_id)
    dst_balances = RelayerHelper.QueryBalance(dst_id)
    print(f"All tokens transfers were atpemted from {src_id} to {dst_id}.")
    print(src_balances)
    print(dst_balances)

    for balance in dst_balances:
        denom=balance["denom"]
        amount=int(balance["amount"])
        if amount <= 2:
            continue
        if not RelayerHelper.TransferTokens(dst_id,src_id,f"1{denom}",src_addr):
            print(f"Failed to send 2{denom} from {dst_id} to {src_id}.")
    
    src_balances = RelayerHelper.QueryBalance(src_id)
    dst_balances = RelayerHelper.QueryBalance(dst_id)
    print(f"All tokens transfers were atpemted from {dst_id} to {src_id}.")
    print(src_balances)
    print(dst_balances)

    #kira-1 and vostok-1

# rly tx transfer kira-1 hashquarkchain 1samoleans true $(rly ch addr hashquarkchain)
# rly tx transfer kira-1 nibiru-ibc 1quark true $(rly ch addr nibiru-ibc)

#connection info
#rly pth show kira-1_hashquarkchain -j

#rly pth delete kira-1_hashquarkchain

######################################## rly paths add kira-1 hashquarkchain kira-1_hashquarkchain
## rly pth gen kira-1 transfer hashquarkchain transfer kira-1_hashquarkchain
# rly tx link kira-1_hashquarkchain

# rly q bal kira-1 -j
# rly q bal hashquarkchain -j

#rly ch addr hashquarkchain

# rly tx transfer hashquarkchain kira-1 1quark true $(rly ch addr kira-1)
# rly tx transfer kira-1 hashquarkchain 1ukex true $(rly ch addr hashquarkchain)