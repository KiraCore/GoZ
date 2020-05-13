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
    path_info = RelayerHelper.QueryPath(path) # rly pth show kira-alpha_kira-1-2 -j
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
        print(f"WARNING: Path {path} is not connected, status: {status}");
        return False
    ttl = RelayerHelper.GetRemainingTimesToLive(connection)
    if ttl == None:
        return None
    if not ttl or ttl["min"] <= 0:
        print(f"WARNING: Path {path} expired, TTL: {ttl}")
        return False
    return True

def UpdateLiteClients(connection):
    return ClientHelper.UpdateLiteClient(connection["src"]) and ClientHelper.UpdateLiteClient(connection["dst"])

def RestartLiteClients(connection):
    return ClientHelper.RestartLiteClient(connection["src"]) and ClientHelper.RestartLiteClient(connection["dst"])

def DeleteLiteClients(connection):
    return ClientHelper.DeleteLiteClient(connection["src"]) and ClientHelper.DeleteLiteClient(connection["dst"])

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
            if not RelayerHelper.TransactClients(path, timeout): # rly transact clients kira-alpha_kira-1-2 --debug
                print(f"ERROR: Failed to create clients (Step 1) between {chain_id_src} and {chain_id_dst}, path: '{path}'")
                return False
            else:
                print(f"SUCCESS: Established clients (Step 1) between {chain_id_src} and {chain_id_dst}, path: '{path}'")

        if not status["connection"]: 
            if not RelayerHelper.TransactConnection(path, timeout): # rly transact connection kira-alpha_kira-1-2 --debug
                print(f"ERROR: Failed to create connection (step 2) between {chain_id_src} and {chain_id_dst}, path: '{path}'")
                return False
            else:
                print(f"SUCCESS: Established connection (Step 2) between {chain_id_src} and {chain_id_dst}, path: '{path}'")

        if not status["channel"]: # rly transact channel kira-alpha_kira-1-2 --debug
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

    if not ReArmConnection(connection, timeout):
        print(f"WARNING: Failed to rearm {path} connection")
    else:
        print(f"SUCCESS, connection was re-armed. Status: {QueryStatus(path)}")

    if not RestartLiteClients(connection): # it should always be possible to restart lite clients
        raise Exception(f"Could NOT restart lite clients, it will not be possible to connect")

    ttl = RelayerHelper.GetRemainingTimesToLive(connection) 
    if None != ttl and ttl["min"] < min_ttl: # connection expired
        print(f"WARNING: Path {path} expired, TTL: {ttl}")
        RelayerHelper.DeletePath(path)
        connection["path-info"] = None
        return Connect(connection, timeout)
    elif ttl == None:
        raise Exception(f"Failed to read TTL")

    if not IsConnected(connection):
        raise Exception(f"Failed to connect {chain_id_src} and {chain_id_dst} via {path}")

    connection["ttl"] = ttl = RelayerHelper.GetRemainingTimesToLive(connection)
    if not ttl: # Assert there are no networking issues, NOTE: Auto rotate RPC add should occur before this section
        raise Exception(f"Failed to acquire TTL information of chain {chain_id_src} and {chain_id_dst} connected via {path} path")

    print(f"SUCCESS: Chains {chain_id_src} and {chain_id_dst} are connected, TTL: {ttl}")
    connection["path-info"] = path_info = RelayerHelper.QueryPath(path) # rly pth show kira-alpha_gameofzoneshub-1 -j

    if not path_info: # assert path info availability
        raise Exception(f"Failed to acquire path information of a successfully connected chain {chain_id_src} and {chain_id_dst} connected via {path}")

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
    connection = { "path": path, "min-ttl": min_ttl }
    # Initialize Source
    connection["src"] = src_chain_info = ClientHelper.InitializeClientWithJsonFile(src_json_path, key_prefix, scr_mnemonic, bucket)
    print(f"SUCCESS: Source client {src_chain_info['chain-id']} was initalized")
    # Initialize Destination
    connection["dst"] = dst_chain_info = ClientHelper.InitializeClientWithJsonFile(dst_json_path, key_prefix, dst_mnemonic, bucket)
    print(f"SUCCESS: Destination client {dst_chain_info['chain-id']} was initalized")
    # this command is asserted and throws if connection is not estbalished
    return Connect(connection, timeout) 

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
    min_ttl = connection["min-ttl"]

    if not RelayerHelper.UpdateLiteClient(src_id) or (not RelayerHelper.QueryLiteClientHeader(src_id)):
        print(f"FAILURE: Could not update source '{src_id}' lite client or fetch header")
        return False
    if not RelayerHelper.UpdateLiteClient(dst_id) or (not RelayerHelper.QueryLiteClientHeader(dst_id)):
        print(f"FAILURE: Could not update destination '{dst_id}' lite client or fetch header")
        return False

    status = QueryStatus(path)
    is_connected = TestStatus(status)
    ttl = RelayerHelper.GetRemainingTimesToLive(connection)

    if is_connected:
        print(f"SUCCESS: Connection of the path {path} is maitained, testing ttl...")
        if not ttl or ttl["min"] <= 0:
            print(f"FAILURE: Could not acquire remaining TTL or {ttl} indicates dropped connection.")
            is_connected = False
    else:
        print(f"FAILURE: Connection of the path {path} is faulty.")

    if None != status:
        print(f"INFO: Path {path} status: Chains {status['chains']} | Clients {status['clients']} | Connection {status['connection']} | Channel {status['channel']}, TTL: {ttl}")
    else:
        print(f"WARNING: Failed to query connection status")

    return is_connected

def GasUpdateAsserts(connection, gas):
    return ClientHelper.GasUpdateAssert(connection["src"], gas) and ClientHelper.GasUpdateAssert(connection["dst"], gas)

