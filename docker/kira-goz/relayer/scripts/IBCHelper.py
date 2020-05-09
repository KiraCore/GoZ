import RelayerHelper
import ClientHelper
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

# Update: (rm $SELF_SCRIPTS/IBCHelper.py || true) && nano $SELF_SCRIPTS/IBCHelper.py 

def QueryStatus(path):
    path_info = RelayerHelper.QueryPath(path) # rly pth show kira-alpha_kira-1 -j
    status = None if (not path_info) else path_info["status"]
    return status

def TestStatus(status):
    if not status:
        return False
    return False if (not status) else (status["chains"] and status["clients"] and status["connection"] and status["channel"])

# Returns None if its not not known if connection exists (networking issues) else False or True
def IsConnected(connection):
    path=connection["path"]
    status = QueryStatus(path)
    if status == None:
        return None
    if not TestStatus(status):
        return False
    ttl = RelayerHelper.GetRemainingTimeToLive(connection)
    if ttl == None:
        return None
    if not ttl or ttl["min"] <= 0:
        print(f"WARNING: Path {path} expired, TTL: {ttl}")
        return False
    return True

def UpdateLiteClients(connection):
    chain_id_src=connection["src"]["chain-id"]
    chain_id_dst=connection["dst"]["chain-id"]
    print(f"INFO: Updating lite clients...")
    if not RelayerHelper.UpdateLiteClient(chain_id_src):
        print(f"ERROR: Failed to update {chain_id_src} lite client")
        return False
    else:
        print(f"SUCCESS: Updated {chain_id_src} lite client")
    if not RelayerHelper.UpdateLiteClient(chain_id_dst):
        print(f"ERROR: Failed to update {chain_id_dst} lite client")
        return False
    else:
        print(f"SUCCESS: Updated {chain_id_dst} lite client")
    return True

def RestartLiteClients(connection):
    chain_id_src=connection["src"]["chain-id"]
    chain_id_dst=connection["dst"]["chain-id"]
    print(f"INFO: Re-starting lite clients...")
    if not RelayerHelper.RestartLiteClient(chain_id_src):
        print(f"ERROR: Failed to update {chain_id_src} lite client")
        return False
    else:
        print(f"SUCCESS: Updated {chain_id_src} lite client")
    if not RelayerHelper.RestartLiteClient(chain_id_dst):
        print(f"ERROR: Failed to update {chain_id_dst} lite client")
        return False
    else:
        print(f"SUCCESS: Updated {chain_id_dst} lite client")
    return True

def DeleteLiteClients(connection):
    chain_id_src=connection["src"]["chain-id"]
    chain_id_dst=connection["dst"]["chain-id"]
    print(f"INFO: Re-starting lite clients...")
    if not RelayerHelper.DeleteLiteClient(chain_id_src):
        print(f"ERROR: Failed to update {chain_id_src} lite client")
        return False
    else:
        print(f"SUCCESS: Updated {chain_id_src} lite client")
    if not RelayerHelper.DeleteLiteClient(chain_id_dst):
        print(f"ERROR: Failed to update {chain_id_dst} lite client")
        return False
    else:
        print(f"SUCCESS: Updated {chain_id_dst} lite client")
    return True

def ReArmConnection(connection, timeout):
    print(f"INFO: Re-arming connection...")
    chain_info_src=connection["src"]
    chain_info_dst=connection["dst"]
    chain_id_src = chain_info_src["chain-id"]
    chain_id_dst = chain_info_dst["chain-id"]
    path = connection["path"]

    print(f"INFO: Updating lite clients...")
    if not UpdateLiteClients(connection):
        print(f"WARNING: Failed to update lite clients, restarting...")
        if not RestartLiteClients(connection):
             raise Exception(f"Failed to restart lite clients, connection can't be established, exiting...")

    status = QueryStatus(path)

    if TestStatus(status):
         print(f"INFO: Path {path} was already connected")
         return True
    
    if (not (not status)):
        print(f"INFO: Path {path} status: Chains {status['chains']} | Clients {status['clients']} | Connection {status['connection']} | Channel {status['channel']}")

        if not status["clients"]: 
            if not RelayerHelper.TransactClients(path, timeout): # rly transact clients kira-alpha_hashquarkchain --debug
                print(f"ERROR: Failed to create clients (Step 1) between {chain_id_src} and {chain_id_dst}, path: '{path}'")
                return False
            else:
                print(f"SUCCESS: Established clients (Step 1) between {chain_id_src} and {chain_id_dst}, path: '{path}'")

        if not status["connection"]: 
            if not RelayerHelper.TransactConnection(path, timeout): # rly transact connection kira-alpha_hashquarkchain --debug
                print(f"ERROR: Failed to create connection (step 2) between {chain_id_src} and {chain_id_dst}, path: '{path}'")
                return False
            else:
                print(f"SUCCESS: Established connection (Step 2) between {chain_id_src} and {chain_id_dst}, path: '{path}'")

        if not status["channel"]: # rly transact channel kira-alpha_hashquarkchain --debug
            if not RelayerHelper.TransactChannel(path, timeout):
                print(f"ERROR: Failed to create channel (step 3) between {chain_id_src} and {chain_id_dst}, path: '{path}'")
                return False
            else:
                print(f"SUCCESS: Established channel (Step 3) between {chain_id_src} and {chain_id_dst}, path: '{path}'")
    return True

# Interacts with configuration file: $HOME/.relayer/config/config.yaml
def ShutdownConnection(connection):
    chain_info_src=connection.get("src", None)
    chain_info_dst=connection.get("dst", None)
    chain_id_src =  None if not chain_info_src else chain_info_src["chain-id"]
    chain_id_dst =  None if not chain_info_dst else chain_info_dst["chain-id"]
    path = connection.get("path", f"{chain_id_src}_{chain_id_dst}") # delete default path if custom one was not defined
    if path: # rly pth delete kira-alpha_gameofzoneshub-1 | rly pth delete kira-1_kira-alpha
        print(f"INFO: Shutting down {path} connection...") 
        RelayerHelper.DeletePath(path) 
    else:
        print(f"WARNING: Path was not present in the connection object, can't remove None")
    if chain_info_src and len(chain_info_src) > 0:
        ClientHelper.ShutdownClient(chain_info_src)
    else:
        print(f"WARNING: Source chain was not present in the connection object, can't remove None")
    if chain_info_dst and len(chain_info_dst) > 0:
        ClientHelper.ShutdownClient(chain_info_dst)
    else:
        print(f"WARNING: Destination chain not present in the connection object, can't remove None")


def Connect(connection, timeout):
    chain_info_src=connection["src"]
    chain_info_dst=connection["dst"]
    connection["success"] = False
    
    chain_id_src = chain_info_src["chain-id"]
    chain_id_dst = chain_info_dst["chain-id"]
    path = connection["path"];
    min_ttl = connection["min-ttl"]
    path_info = connection.get("path-info", None)
    

    if (chain_id_src == chain_id_dst):
        raise Exception(f"Source chain and destination chain id's cant be the same, but both were: {chain_id_src}")
        return connection
    
    if not RelayerHelper.PathExists(path):
        DeleteLiteClients(connection)
        if (not (not path_info)):
            print(f"INFO: Path {path} does not exists, but recovery state is available")
            RelayerHelper.AddPath(connection)
        else:
            print(f"INFO: Path {path} does not exists and recovery is not available, re-generating path")
            if not RelayerHelper.ReGeneratePath(chain_id_src,chain_id_dst,path): 
                raise Exception(f"Failed to re-generate new {path} path")
            else:
                connection["path-info"] = path_info = None
    
    if not RelayerHelper.PathExists(path): # by now path must exist
        raise Exception(f"Failed to assert {path} path existence") # probably networking issues

    if not RestartLiteClients(connection): # it should always be possible to restart lite clients
        raise Exception(f"Could NOT restart lite clients, it will not be possible to connect")

    if not ReArmConnection(connection, timeout):
        ttl = RelayerHelper.GetRemainingTimeToLive(connection) 
        if None != ttl and ttl["min"] < min_ttl: # connection expired
            print(f"WARNING: Path {path} expired, TTL: {ttl}")
            RelayerHelper.DeletePath(path)
            connection["path-info"] = None
            return Connect(connection, timeout)
        else:
            raise Exception(f"Failed to re-arm connection via {path} path")

    connection["success"] = success = IsConnected(connection)
    if not success:
        raise(f"Failed to connect {chain_id_src} and {chain_id_dst} via {path}")

    connection["ttl"] = ttl = RelayerHelper.GetRemainingTimeToLive(connection)
    if not ttl: # Assert there are no networking issues, NOTE: Auto rotate RPC add should occur before this section
        raise(f"Failed to acquire TTL information of chain {chain_id_src} and {chain_id_dst} connected via {path} path")

    print(f"SUCCESS: Chains {chain_id_src} and {chain_id_dst} are connected, TTL: {ttl}")
    connection["path-info"] = path_info = RelayerHelper.QueryPath(path) # rly pth show kira-alpha_gameofzoneshub-1 -j

    if not path_info: # assert path info availability
        raise(f"Failed to acquire path information of a successfully connected chain {chain_id_src} and {chain_id_dst} connected via {path}")

    return connection

def ReConnect(connection, timeout):
    chain_info_src=connection["src"]
    chain_info_dst=connection["dst"]
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

    return Connect(connection, timeout)

def ConnectWithJson(src_json_path, scr_mnemonic, dst_json_path, dst_mnemonic, bucket, path, key_prefix, timeout, min_ttl):
    print(f"INFO: Started => ConnectWithJson({src_json_path},{dst_json_path})")
    connection = { "success": False, "path": path, "min-ttl": min_ttl }

    connection["src"] = src_chain_info = ClientHelper.InitializeClientWithJsonFile(src_json_path, key_prefix, scr_mnemonic, bucket)
    src_chain_id = src_chain_info["chain-id"]
    print(f"SUCCESS: Source client {src_chain_id} was initalized")

    connection["dst"] = dst_chain_info = ClientHelper.InitializeClientWithJsonFile(dst_json_path, key_prefix, dst_mnemonic, bucket)
    dst_chain_id = dst_chain_info["chain-id"]
    print(f"SUCCESS: Destination client {dst_chain_id} was initalized")
    
    src_address = src_chain_info["address"]
    connection["src"] = src_chain_info

    dst_address = dst_chain_info["address"]
    connection["dst"] = dst_chain_info

    src_fee_token_amount = RelayerHelper.GetAmountByDenom(src_chain_info["balance"], src_denom)
    dst_fee_token_amount = RelayerHelper.GetAmountByDenom(dst_chain_info["balance"], dst_denom)
    print(f"INFO: Source client balance {src_chain_id} ({src_address}): {src_fee_token_amount} {src_denom}")
    print(f"INFO: Destination client balance {dst_chain_id} ({dst_address}): {dst_fee_token_amount} {dst_denom}")
    return Connect(connection, timeout) # this command is asserted and throws if connection is not estbalished

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

def TestConnection(connection):
    src_chain_info = connection["src"]
    dst_chain_info = connection["dst"]
    src_id = src_chain_info["chain-id"]
    dst_id = dst_chain_info["chain-id"]
    path = connection["path"]

    RelayerHelper.InitLiteClient(src_id)
    RelayerHelper.InitLiteClient(dst_id)
    src_header = RelayerHelper.QueryLiteClientHeader(src_id)
    dst_header = RelayerHelper.QueryLiteClientHeader(dst_id)
    status = QueryStatus(path)
    is_connected = TestStatus(status)

    if is_connected:
        print(f"SUCCESS: Connection of the path {path} is maitained.")
    else:
        print(f"FAILURE: Connection of the path {path} is faulty.")

    if None != status:
        print(f"INFO: Path {path} status: Chains {status['chains']} | Clients {status['clients']} | Connection {status['connection']} | Channel {status['channel']}")
    else:
        print(f"WARNING: Failed to query connection status")

    return is_connected
