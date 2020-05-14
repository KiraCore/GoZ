import TaskHelper
import IBCHelper
import ClientHelper
import StringHelper
import multiprocessing
import ArrayHelper
import subprocess
import json
import statistics
import sys
import os
import ast
import os.path
import time
import datetime
import dateutil.parser
from datetime import datetime, timezone
from joblib import Parallel, delayed
from subprocess import Popen, PIPE

# Update: (rm $SELF_SCRIPTS/RelayerHelper.py || true) && nano $SELF_SCRIPTS/RelayerHelper.py

def callRaw(s, showErrors):
    err = None
    try:
        #print(f"callRaw => Input: {s}") # debug only
        o = TaskHelper.CMD(s, 3600)
        #print(f"callRaw => Output: {o}") # debug only
        return o.encode("utf-8")
    except Exception as e:
        pass
        #print(f"callRaw => Error: {str(e)}") # debug only
        if showErrors:
            print(f"ERROR: CMD {str(e)}")
        return None

def callJson(s, showErrors):
    jsonParseError = False
    o = None
    try:
        o = TaskHelper.CMD(s, 3600)
        jsonParseError = False
        j = json.loads(o)
        if type(j) == str:
            return ast.literal_eval(j) # json.loads(o,encoding="utf-8")
        else:
            return j
    except Exception as e:
        pass
        if showErrors:
            if jsonParseError:
                print(f"CMD '{s}' failed to parse output: '{str(o)}', error: {str(e)}")
            else:
                print(f"ERROR: CMD {str(e)}")
        return None

def callRawInput(s, input, showErrors):
    err = None
    try:
        return TaskHelper.CMDInput(s, input, 3600)
    except Exception as e:
        pass
        #print(f"callRaw => Error: {str(e)}") # debug only
        if showErrors:
            print(f"ERROR: CMD {str(e)}")
        return None

def callTryRetry(s, timeout, retry, delay, showErrors):
    return TaskHelper.TryRetryCMD(s, timeout, retry, delay, showErrors)

def callTryRetryJson(s, timeout, retry, delay, showErrors):
    return TaskHelper.TryRetryCMD(s, timeout, retry, delay, showErrors)

def ConfigureDefaultKey(chain_id, key_name): # rly ch edit kira-1 key prefix_kira-1
    return False if (None == callRaw(f"rly ch edit {chain_id} key {key_name}",True)) else True 

def ConfigureDefaultGas(chain_id, gas_value): # rly ch edit kira-1 gas 1000000
    return False if (None == callRaw(f"rly ch edit {chain_id} gas {gas_value}",True)) else True 

def ChainDelete(chain_id):
    return False if (None == callRaw(f"rly chains delete {chain_id}",True)) else True

def ShowChain(chain_id):
    return callJson(f"rly ch show {chain_id} -j", True)

def TryShowChain(chain_id):
    chain_info = callJson(f"rly ch show {chain_id} -j", False)
    return None if ((not chain_info) or (len(chain_info) <= 0)) else chain_info

def TryQueryChainAddress(chain_id):
    out = callRaw(f"rly ch address {chain_id}", False)
    return None if ((not out) or (len(out) <= 0)) else out

def IsKeyConfigured(chain_id):
    out = TryQueryChainAddress(chain_id)
    return False if ((not out) or (len(out) <= 0)) else True

def AddChainFromFile(chain_info_path):
    return False if (None == callRaw(f"rly ch add -f {chain_info_path}",True)) else True

def UpsertChainFromFile(chain_info_path):
    chain_info = json.load(open(chain_info_path))
    chain_id = chain_info["chain-id"]
    if None != callRaw(f"rly ch show {chain_id} -j", False): # chain DO exists
        print(f"INFO: Chain {chain_id} already exists so will be removed and re-added.")
        if not ChainDelete(chain_id):
            print(f"WARNING: Failed to remove {chain_id}")
    return AddChainFromFile(chain_info_path)

def DeleteLiteClient(chain_id):
    return False if (None == callRaw(f"rly lite delete {chain_id}",True)) else True

def InitLiteClient(chain_id):
    return False if (None == callRaw(f"rly lite init {chain_id} -f",True)) else True

def UpdateLiteClient(chain_id):
    return False if (None == callRaw(f"rly lite update {chain_id}",True)) else True

def QueryLiteClientHeader(chain_id):
    if None == callRaw(f"rly lite update {chain_id}",False): # lite must be updated before the query
        return None
    out = callJson(f"rly lite header {chain_id}",True)
    return None if ((None != out) and len(out) <= 0) else out

def QueryClient(chain_id, client_id):
    out = callJson(f"rly q client {chain_id} {client_id}",True)
    return None if ((None != out) and len(out) <= 0) else out

def TryRequestTokens(chain_id):
    return False if (None == callTryRetry(f"rly testnets request {chain_id}", 60, 1, 0, False)) else True

def RequestTokens(chain_id):
    return False if (None == callRaw(f"rly testnets request {chain_id}",True)) else True

def RequestTokens_Process(chain_id, timeout, retry, delay):
    return False if (None == callTryRetry(f"rly testnets request {chain_id}", timeout, retry, delay,True)) else True

def TransferTokens(src_chain_id, dst_chain_id, amount, dst_chain_addr, path): # rly tx transfer hashquarkchain kira-1 1quark true $(rly ch addr kira-1)
    return False if (None == callRaw(f"rly tx transfer {src_chain_id} {dst_chain_id} {amount} true {dst_chain_addr} --path={path}",True)) else True

def TransferTokensInternally(src_chain_info, dst_chain_info, amount, path):
    src_id = src_chain_info["chain-id"]
    dst_id = dst_chain_info["chain-id"]
    dst_addr = dst_chain_info["address"]
    s = f"rly tx transfer {src_id} {dst_id} {amount} true {dst_addr} --path={path}"
    out = callRaw(s, True)
    if out == None:
        return None
    if "err(" in f"{out}":
        print(f"ERROR: Token transfer failed: {s} => {out}")
    return out

def SendPacket(src_chain_info, dst_chain_info, path, data):
    src_id = src_chain_info["chain-id"]
    dst_id = dst_chain_info["chain-id"]
    return callRaw(f"rly tx transfer {src_id} {dst_id} {data} --path={path}", True);

def TryQueryBalance(chain_id):
    balance=callJson(f"rly q bal {chain_id} -j", False)
    return None if ((None != balance) and (len(balance) <= 0)) else balance

def DeletePath(path):
    return False if (None == callRaw(f"rly pth delete {path}",True)) else True

def PathExists(path): # rly pth show kira-alpha_kira-1-1b -j
    return False if not callJson(f"rly pth show {path} -j",False) else True

def GeneratePath(chain_id_src, chain_id_dst, path):
    if PathExists(path):
        return True #path was already created
    out=callRaw(f"rly pth gen {chain_id_src} transfer {chain_id_dst} transfer {path} --debug",True)
    return PathExists(path)

def ReGeneratePath(chain_id_src, chain_id_dst, path):
    callRaw(f"rly pth delete {path}",False) # lets delete path to be for sure on the safe side if something goes wrong
    out=callRaw(f"rly pth gen {chain_id_src} transfer {chain_id_dst} transfer {path} -f --debug",True)
    return PathExists(path)

def QueryChainAddress(chain_id):
    out=callRaw(f"rly ch addr {chain_id}",True)
    return None if ((None != out) and len(out) <= 0) else out

'''
# Example Output:
{"chains":{
 "src":{"chain-id":"kira-alpha","client-id":"ubohltylat","connection-id":"tdeeqbwuau","channel-id":"ejjggqwtkm","port-id":"transfer","order":"ORDERED"},
 "dst":{"chain-id":"kira-1","client-id":"mbxdppcthy","connection-id":"wqvfpxjmzy","channel-id":"qzjrrvnwzn","port-id":"transfer","order":"ORDERED"},
 "strategy":{"type":"naive"}},
 "status":{"chains":true,"clients":true,"connection":true,"channel":true}}
'''
def QueryPath(path):
    out=callJson(f"rly pth show {path} -j",True)
    return None if ((None != out) and len(out) <= 0) else out

def AddPath(connection):
    s=connection["src"]["chain-id"] ; d=connection["dst"]["chain-id"]
    p=connection["path"]
    srcPI=connection["path-info"]["src"] ; dtsPI=connection["path-info"]["dst"]
    s_ci=srcPI["client-id"] ; s_cn=srcPI["connection-id"] ; s_ch=srcPI["channel-id"] ; s_cp=srcPI["port-id"]
    d_ci=dstPI["client-id"] ; d_cn=dstPI["connection-id"] ; d_ch=dstPI["channel-id"] ; d_cp=dstPI["port-id"]
    out=callRawInput(f"rly pth add {s} {d} {p}", "{s_ci}\n{s_cn}\n{s_ch}\n{s_cp}\n{d_ci}\n{d_cn}\n{d_ch}\n{d_cp}\n" ,True)
    path = QueryPath(p)
    if not path:
        return False
    ps = path["src"] ; pd = path["dst"]
    return \
    ps["client-id"] == s_ci and pd["client-id"] == d_ci and \
    ps["connection-id"] == s_cn and pd["connection-id"] == d_cn and \
    ps["channel-id"] == s_ch and pd["channel-id"] == d_ch and \
    ps["port-id"] == s_cp and pd["port-id"] == d_cp

def TransactClients(path,timeout):
    return False if (None == callTryRetry(f"rly transact clients {path}",timeout, 2, 1,True)) else True

def TransactConnection(path, timeout):
    return False if (None == callTryRetry(f"rly transact connection {path}",timeout, 2, 1,True)) else True

def TransactChannel(path, timeout):
    return False if (None == callTryRetry(f"rly transact channel {path}",timeout, 2, 1,True)) else True

def TransactLink(path, timeout):
    return False if (None == callTryRetry(f"rly transact link {path}",timeout, 2, 1,True)) else True

# relay any packets that remain to be relayed on a given path, in both directions
def TransactRelay(path): # rly tx rly kira-alpha_isillienchain
    return True if (None == callRaw(f"rly transact relay {path}",True)) else False

def GetAmountByDenom(balances, denom):
    amount = 0
    if balances and (len(balances) > 0):
        for balance in balances:
            if (not balance) or (balance["denom"] != denom):
                continue
            else:
                amount = int(balance["amount"])
    return amount

def KeyExists(chain_id, key_name): # rly keys show kira-alpha test_key_kira-alpha
    out = callRaw(f"rly keys show {chain_id} {key_name}", False)
    return False if (None == out) else True

def ShowKey(chain_id, key_name): # rly keys show kira-1 prefix_kira-1
    out = callRaw(f"rly keys show {chain_id} {key_name}", True)
    return None if (None == out) else out

# if key exists - deletes key, else returns true and try delete if key is already gone
def DeleteKey(chain_id, key_name): # rly keys delete kira-alpha test_key_kira-alpha
    if KeyExists(chain_id, key_name):
        callRaw(f"rly keys delete {chain_id} {key_name}", True)
    else:
        callRaw(f"rly keys delete {chain_id} {key_name}", False) # just to be sure try kill the key
    return KeyExists(chain_id, key_name)

def RestoreKey(chain_id, key_name, mnemonic):
    return None if (None == callRaw(f"rly keys restore {chain_id} {key_name} '{mnemonic}'",True)) else True

def UpsertKey(chain_id, key_name):
    return callRaw(f"rly keys add {chain_id} {key_name}",True) # rly keys add kira-alpha prefix_kira-alpha

def RelayPendingTransactions(path): # rly tx rly goz_alpha_v1 --debug
    pending = callRaw(f"rly tx rly {path}", True)
    if pending == None:
        return False
    return CountPendingTransactions(path) <= 0

def QueryPendingTransactions(path):
    return callJson(f"rly q unrelayed {path}",True) # rly q unrelayed goz_alpha_v1

def CountPendingTransactions(path):
    pending = QueryPendingTransactions(path)
    if None == pending:
        raise Exception("Failed to query pending transactions of the {path} path")
    src_pending=len(pending.get("src",[]))
    dst_pending=len(pending.get("dst",[]))
    return src_pending + dst_pending

def PushPendingTransactions(path):
    pending = CountPendingTransactions(path)
    if pending > 0:
        print(f"INFO: Found {pending} pending transactions in {path} path")
        return RelayPendingTransactions(path)
    else:
        print(f"INFO: No pending transactions were found in path {path}")
        return True

def RestartLiteClient(chain_id):
    callRaw(f"rly lite delete {chain_id}",False) # rly lite delete kira-1
    callRaw(f"rly lite update {chain_id}",False) # rly lite init kira-1 -f
    callRaw(f"rly lite init {chain_id} -f",False) # rly lite update kira-1
    out = QueryLiteClientHeader(chain_id) # rly lite header kira-1
    return False if not out else True

def UpdateLiteClient(chain_id):
    if (None == callRaw(f"rly lite update {chain_id}",False)):
        if (None == callRaw(f"rly lite init {chain_id} -f",False)):
            return False
        if (None != callRaw(f"rly lite update {chain_id}",False)):
            out = QueryLiteClientHeader(chain_id) # rly lite header kira-1
            return False if not out else True
        else:
            return False
    else:
        return True

def GetRemainingTimesToLive(connection):
    p=connection["path"]
    path_info = QueryPath(p) # rly pth show $p -j
    if not path_info:
        print("ERROR: Could NOT read connection time, failed to query path {p}")
        return None

    src_chain_info = connection["src"]
    dst_chain_info = connection["dst"]
    src_chain_id = src_chain_info["chain-id"]
    dst_chain_id = dst_chain_info["chain-id"]
    src_client_id = path_info["chains"]["src"]["client-id"]
    dst_client_id = path_info["chains"]["dst"]["client-id"]
    
    src_client_info = QueryClient(src_chain_id, src_client_id) # rly q client $s
    if not src_client_info: # rly q client kira-alpha upiobaeidw
        print(f"ERROR: Could NOT read connection time, failed to query source client {src_chain_id} ({src_client_id})")
        return None

    dst_client_info = QueryClient(dst_chain_id, dst_client_id) # rly q client $s
    if not dst_client_info: # rly q client kira-1 upiobaeidw
        print(f"ERROR: Could NOT read connection time, failed to query destination client {dst_chain_id} ({dst_client_id})")
        return None

    time_now = datetime.utcnow()
    src_ttl = -1 ; dst_ttl = -1 # time remaining source & destination
    try:
        src_datetime=src_client_info["client_state"]["value"]["last_header"]["signed_header"]["header"]["time"]
        src_trusting_period=int(src_client_info["client_state"]["value"]["trusting_period"][:-9]) # nanoseconds 10^9
        src_elapsed = (time_now - dateutil.parser.isoparse(src_datetime).replace(tzinfo=None)).total_seconds()
        src_ttl = int(src_trusting_period - src_elapsed)
        if src_ttl <= 0:
            raise Exception(f"Trusing period of the source chain {src_chain_id} expired. Time: {src_datetime}, Trusting: {src_trusting_period}, Elapsed: {src_elapsed}, Remaining: {src_ttl}")
    except  Exception as e:
        pass
        print(f"WARNING: Could NOT find last signed header time of the source chain {src_chain_id}: {str(e)}")
    
    try:
        dst_datetime=dst_client_info["client_state"]["value"]["last_header"]["signed_header"]["header"]["time"]
        dst_trusting_period=int(dst_client_info["client_state"]["value"]["trusting_period"][:-9]) # nanoseconds 10^9
        dst_elapsed = (time_now - dateutil.parser.isoparse(dst_datetime).replace(tzinfo=None)).total_seconds()
        dst_ttl = int(dst_trusting_period - dst_elapsed)

        if dst_ttl <= 0:
            raise Exception(f"Trusing period of the destination chain {dst_chain_id} expired. Time: {dst_datetime}, Trusting: {dst_trusting_period}, Elapsed: {dst_elapsed}, Remaining: {dst_ttl}")
    except Exception as e:
        pass
        print(f"WARNING: Could NOT find last signed header time of the destination {dst_chain_id} chain: {str(e)}")
    
    return { "src": src_ttl, "dst": dst_ttl, "min": min(src_ttl,dst_ttl), "max": max(src_ttl,dst_ttl) } 
    
    
# Usage: rly transact raw update-client [src-chain-id] [dst-chain-id] [client-id] [flags]
# rly pth show kira-alpha_kira-1 -j
# rly transact raw update-client kira-alpha kira-1 nhzihoslfo --debug
# rly transact link kira-alpha_kira-1
def UpdateClientConnection(chain_info, path):    
    info = QueryPath(path) # rly pth show $p -j
    if not info or (not info["chains"]) or (not info["status"]):
        print(f"ERROR: Could not correctly query path {path}, chain or status information is missing from the response")
        return False

    chains = info["chains"]
    status = info["status"]
    is_connected = IBCHelper.TestStatus(status)
    
    if not is_connected:
        print(f"WARNING: Chains are not connected, might not be able to propagate transactions")
    #    print(f"ERROR: Could not update client connection because path {path} does not have established connection")
    #    return False
    
    chain_id = chain_info["chain-id"]
    src_chain_id = chains["src"]["chain-id"]
    dst_chain_id = chains["dst"]["chain-id"]
    is_source = src_chain_id == chain_id
    is_destination = dst_chain_id == chain_id

    if (not is_source) and (not is_destination):
        print(f"ERROR: Chain {chain_id} is nither a source nor destination of the path '{path}'")
        return False

    client_id = None
    if is_source:
        client_id = chains["src"]["client-id"]
    else:
        client_id = chains["dst"]["client-id"]
        tmp = dst_chain_id
        dst_chain_id = src_chain_id
        src_chain_id = tmp

    depth_now=0
    depth_max=100
    gas_min = chain_info.get("gas-min", 0)
    while True:
        depth_now = depth_now + 1

        if depth_now > depth_max: # ensure that loop is not infinite
            raise  Exception(f"Maximum recursion depth {depth_max} exceeded")

        tx = callJson(f"rly transact raw update-client {src_chain_id} {dst_chain_id} {client_id}", True)
        if (None == tx):
            print(f"ERROR: Client was NOT updated")
            return False
        if int(tx.get("height", "0")) <= 0: # something went wrong
            print(f"ERROR: Failed to propagate raw update-client transactions between {src_chain_id} and {dst_chain_id} with client-id {client_id}, tx response: {tx}")
            gas_used=int(tx.get("gas_used", f"{gas_min}"))
            gas_wanted=int(tx.get("gas_wanted", f"{gas_min}"))
            
            if gas_used > 0 and gas_used > gas_wanted: # update gas if our of gas
                print(f"WARNING: Out of gas, increasing from {gas_wanted} to {gas_used}")
                ClientHelper.GasUpdateAssert(chain_info, gas_used + 1000)
                continue
            
            return False
    print(f"SUCCESS: Client was updated: {tx}")
    return True