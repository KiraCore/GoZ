
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



#ext_chains_info = {}
#
## interate all config files
#for filename in os.listdir(DESTINATION_RLYS_DIR):
#    file_dir=f"{DESTINATION_RLYS_DIR}/{filename}"
#    print(f"Loading... {file_dir}")
#
#    # use diffrent key for each chain
#    # ext_chain_info = FaucetHelper.ClaimTokens(file_dir,None,BUCKET)
#    # use same key for each chain
#    ext_chain_info = FaucetHelper.ClaimTokens(file_dir,RLYKEY_MNEMONIC,BUCKET)
#    if not ext_chain_info:
#        continue
#
#    balance = ext_chain_info["balance"]
#    denom = ext_chain_info["default-denom"]
#    amount = RelayerHelper.GetAmountByDenom(balance, denom)
#
#    ext_chain_id = None
#    if amount > 0:
#       ext_chain_id = ext_chain_info["chain-id"]
#       ext_chains_info[f"{ext_chain_id}"]=ext_chain_info
#    else:
#       print(f"Insufficient token balance, skipping connection...")
#       continue
#
#    chain_id = ext_chain_id
#    chain_info = ext_chain_info
#
##############################################################################################################
#    connections={}
##for chain_id in ext_chains_info:
##    chain_info=ext_chains_info[f"{chain_id}"]
#    print(f"Connecting {base_chain_id} and {chain_id}, timeout 30s ...")
#    connection=IBCHelper.Connect(base_chain_info, chain_info, 30)
#    if ((not connection) or (not connection["success"])):
#        print(f"Skipping token transfer between {base_chain_id} and {chain_id}, connection couldn't be established.")
#        continue
#
#    path=connection["path"]
#    connections[f"{path}"]=connection
#    print(f"SUCCESS!!! connected {base_chain_id} and {chain_id}")
#
#    src = connection["src"]
#    dst = connection["dst"]
#    src_id = src["chain-id"]
#    dst_id = dst["chain-id"]
#    src_addr = src["address"]
#    dst_addr = src["address"]
#    src_balances = RelayerHelper.QueryBalance(src_id)
#    dst_balances = RelayerHelper.QueryBalance(dst_id)
#    
#    print(f"Sending tokens from {src_id} to {dst_id}...")
#    print(src_balances)
#    print(dst_balances)
#    for balance in src_balances:
#        denom=balance["denom"]
#        amount=int(balance["amount"])
#        if amount <= 3:
#            continue
#        if not RelayerHelper.TransferTokens(src_id,dst_id,f"2{denom}",dst_addr):
#            print(f"Failed to send 2{denom} from {src_id} to {dst_id}.")
#        
#    src_balances = RelayerHelper.QueryBalance(src_id)
#    dst_balances = RelayerHelper.QueryBalance(dst_id)
#    print(f"All tokens transfers were atpemted from {src_id} to {dst_id}.")
#    print(src_balances)
#    print(dst_balances)
#
#    for balance in dst_balances:
#        denom=balance["denom"]
#        amount=int(balance["amount"])
#        if amount <= 2:
#            continue
#        if not RelayerHelper.TransferTokens(dst_id,src_id,f"1{denom}",src_addr):
#            print(f"Failed to send 2{denom} from {dst_id} to {src_id}.")
#    
#    src_balances = RelayerHelper.QueryBalance(src_id)
#    dst_balances = RelayerHelper.QueryBalance(dst_id)
#    print(f"All tokens transfers were atpemted from {dst_id} to {src_id}.")
#    print(src_balances)
#    print(dst_balances)
#
#    #kira-1 and vostok-1
#
## rly tx transfer kira-1 hashquarkchain 1samoleans true $(rly ch addr hashquarkchain)
## rly tx transfer kira-1 nibiru-ibc 1quark true $(rly ch addr nibiru-ibc)
#
##connection info
##rly pth show kira-1_hashquarkchain -j
#
##rly pth delete kira-1_hashquarkchain
#
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