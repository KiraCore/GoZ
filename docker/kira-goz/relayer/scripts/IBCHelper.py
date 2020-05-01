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

def QueryStatus(path):
    path_info = RelayerHelper.QueryPath(path) # rly pth show kira-alpha_hashquarkchain -j
    status = None if (not path_info) else path_info["status"]
    return status

def IsConnected(path):
    status = QueryStatus(path)
    connected = False if (not status) else (status["chains"] and status["clients"] and status["connection"] and status["channel"])
    return connected

def UpdateLiteClients(chain_id_src, chain_id_dst, timeout, retry, delay):
    # Update the light options:
    #    1. providing a new root of trust as a --hash/-x and --height
    #    2. via --url/-u where trust options can be found
    #    3. updating from the configured node by passing (no flags) - CURRENT
    if not RelayerHelper.UpdateLiteClient_Process(chain_id_src, timeout, retry, delay): # rly lite update kira-alpha
        print(f"ERROR: Failed to update {chain_id_src} lite client")
        return False
    if not RelayerHelper.UpdateLiteClient_Process(chain_id_dst, timeout, retry, delay): # rly lite update kira-1
        print(f"ERROR: Failed to update {chain_id_dst} lite client")
        return False
    return True

def Connect(chain_info_src, chain_info_dst, timeout):
    connection={}
    connection["src"]=chain_info_src
    connection["dst"]=chain_info_dst
    
    chain_id_src = chain_info_src["chain-id"]
    chain_id_dst = chain_info_dst["chain-id"]
    path=f"{chain_id_src}_{chain_id_dst}"
    connection["path"]=path
    path_info = None

    if (chain_id_src == chain_id_dst):
        print(f"ERROR: source chain and destination chain id's cant be the same ({chain_id_src}")
        return None

    status = QueryStatus(path)
    
    if (not (not status)):
        skip = False # stop step recovery if any of the steps fails
        if (not status["clients"]) and (not RelayerHelper.TransactClients(path)): # rly transact clients kira-alpha_hashquarkchain --debug
            print(f"ERROR: Failed to create clients (Step 1) between {chain_id_src} and {chain_id_dst}, path: '{path}'")
            skip = True
        if (not skip) and (not status["connection"]) and (not RelayerHelper.TransactConnection(path, timeout)): # rly transact connection kira-alpha_hashquarkchain --debug
            print(f"ERROR: Failed to create connection (step 2) between {chain_id_src} and {chain_id_dst}, path: '{path}'")
            skip = True
        if (not skip) and (not status["channel"]) and (not RelayerHelper.TransactChannel(path, timeout)): # rly transact channel kira-alpha_hashquarkchain --debug
            print(f"ERROR: Failed to create channel (step 3) between {chain_id_src} and {chain_id_dst}, path: '{path}'")

    if (not IsConnected(path)):
        RelayerHelper.DeletePath(path) # rly pth delete kira-alpha_hashquarkchain
        if (not RelayerHelper.GeneratePath(chain_id_src,chain_id_dst,path)): #  rly pth gen kira-alpha transfer hashquarkchain transfer kira-alpha_hashquarkchain
            print(f"ERROR: Failed to generate path '{path}' between {chain_id_src} and {chain_id_dst}")
            return None
        if (not RelayerHelper.TransactLink(path, timeout)): # rly transact link kira-alpha_hashquarkchain --timeout 10s
            print(f"ERROR: Failed to link {chain_id_src} and {chain_id_dst} via path '{path}'")

    path_info = RelayerHelper.QueryPath(path) # rly pth show kira-alpha_hashquarkchain -j
    if not path_info:
        print(f"Failed to fetch path info of {path}")
        return None

    connection["info"] = path_info
    connection["success"] = IsConnected(path)
    return connection

def ReConnect(chain_info_src, chain_info_dst, timeout):
    chain_id_src = chain_info_src["chain-id"]
    chain_id_dst = chain_info_dst["chain-id"]
    path=f"{chain_id_src}_{chain_id_dst}"

    status = QueryStatus(path)
    # TO DO disconnect gracefully if status exists
    if (not (not status)):
        print("WARNING! TODO: Disconnect gracefully")
        RelayerHelper.DeletePath(path)
    else:
        RelayerHelper.DeletePath(path)

    return Connect(chain_info_src, chain_info_dst, timeout)

def ConnectWithJson(src_json_path, scr_mnemonic, dst_json_path, dst_mnemonic, bucket, timeout):
    lc_update_retry = 3 # 3x
    lc_update_delay = 5 # 5s

    src_chain_info = FaucetHelper.ClaimTokens(src_json_path, scr_mnemonic, bucket, timeout)
    src_chain_id = src_chain_info["chain-id"]

    if (not src_chain_info["balance"]):
        print(f"Failed to acquire balance information from the source chain '{src_chain_id}', aborting connection...")
        return None
    
    dst_chain_info = FaucetHelper.ClaimTokens(dst_json_path, dst_mnemonic, bucket, timeout)
    dst_chain_id = dst_chain_info["chain-id"]
    
    if (not dst_chain_info) or (not dst_chain_info["balance"]):
        print(f"Failed to acquire balance information from the destination chain '{dst_chain_id}', aborting connection...")
        return None
    
    path = f"{src_chain_id}_{dst_chain_id}"
    
    if not IsConnected(path):
        print(f"Updating lite clients...")
        if not UpdateLiteClients(src_chain_id, dst_chain_id, timeout, lc_update_retry, lc_update_delay):
            print(f"Failed to update lite clients, aborting connection...")
            return None
    
    connection = Connect(src_chain_info, dst_chain_info, timeout)
    
    if (not connection) or (not connection["success"]):
       status = RelayerHelper.QueryPath(path)
       print(f"Failed to establish connection between {src_chain_id} and {dst_chain_id}, status: {status}, aborting connection...")
       return None

    return connection

def TransferEachToken(src_chain_info, dst_chain_info, path, min_amount):
    src_id = src_chain_info["chain-id"]
    dst_id = dst_chain_info["chain-id"]
    src_balance = src_chain_info["balance"]
    dst_balance = dst_chain_info["balance"]
    dst_address = dst_chain_info["address"]

    def Transfer(token):
        amount = 0 if not token["amount"] else int(token["amount"])
        denom = token["denom"]
        if len(denom.split("/")) >= 5:
            print(f"FAILURE: Failed sending {min_amount} {denom} from {src_id} to {dst_id}, tokens with too long paths are not transferable.")
        elif amount <= min_amount:
            print(f"WARNING: Failed sending {min_amount} {denom} from {src_id} to {dst_id}, source address has only {amount} {denom} left.")
        elif (not RelayerHelper.TransferTokens(src_id, dst_id, f"{min_amount}{denom}", dst_address)):
            print(f"FAILURE: Failed sending {min_amount} {denom} from {src_id} to {dst_id}")
        else:
            print(f"SUCCESS: Sent {min_amount}{denom} from {src_id} to {dst_id}")

    if (len(src_balance) <= 0) or (len(dst_balance) <= 0):
        print(f"WARNING: Can't send tokens from {src_id} to {dst_id}, source or destination address does not have any tokens left.")
    else:
        for token in src_balance: #Parallel(n_jobs=max_parallelism)(delayed(Transfer)(token) for token in src_balance)
            Transfer(token)
        
        if not RelayerHelper.TransactRelay(path):
            print(f"ERROR: Failed sending remaining packets")
