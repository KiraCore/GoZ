import TaskHelper
import StringHelper
import multiprocessing
import ArrayHelper
import subprocess
import json
import statistics
import sys
import os
import os.path
import time
from joblib import Parallel, delayed
from subprocess import Popen, PIPE

# Update: (rm $RELAY_SCRIPS/RelayerHelper.py || true) && nano $RELAY_SCRIPS/RelayerHelper.py 

def callRaw(s, showErrors):
    err = None
    try:
        #print(f"callRaw => Input: {s}") # debug only
        o = TaskHelper.CMD(s)
        #print(f"callRaw => Output: {o}") # debug only
        return o
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
        o = TaskHelper.CMD(s)
        jsonParseError = False
        return json.loads(o)
    except Exception as e:
        pass
        if showErrors:
            if jsonParseError:
                print(f"CMD '{s}' failed to parse output: '{str(o)}', error: {str(e)}")
            else:
                print(f"ERROR: CMD {str(e)}")
        return None

def callTryRetry(s, timeout, retry, delay, showErrors):
    return TaskHelper.TryRetryCMD(s, timeout, retry, delay, showErrors)

def ConfigureDefaultKey(chain_id, key_name): # rly ch edit kira-1 key chain_key_kira-1
    return False if (None == callRaw(f"rly ch edit {chain_id} key {key_name}",True)) else True 

def ChainDelete(chain_id):
    return False if (None == callRaw(f"rly chains delete {chain_id}",True)) else True

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
    if None == callRaw(f"rly ch add -f {chain_info_path}", False):
        print(f"WARNING: Chain {chain_id} was already present in the relay and will be updated")
        if not ChainDelete(chain_id):
            print(f"WARNING: Failed to remove {chain_id}")
        else:
            print(f"INFO: Chain {chain_id} was removed the relay and will be updated")
    return AddChainFromFile(chain_info_path)

def DeleteLiteClient(chain_id):
    return False if (None == callRaw(f"rly lite delete {chain_id}",True)) else True

def InitLiteClient(chain_id):
    return False if (None == callRaw(f"rly lite init {chain_id} -f",True)) else True

def InitLiteClient_Process(chain_id, timeout, retry, delay):
    return False if (None == callTryRetry(f"rly lite init {chain_id} -f",timeout,retry,delay,True)) else True

def UpdateLiteClient(chain_id):
    return False if (None == callRaw(f"rly lite update {chain_id}",True)) else True

def UpdateLiteClient_Process(chain_id, timeout, retry, delay):
    return False if (None == callTryRetry(f"rly lite update {chain_id}",timeout,retry,delay,True)) else True

def QueryLiteClientHeader(chain_id):
    out = callJson(f"rly lite header {chain_id}",True)
    return None if ((None != out) and len(out) <= 0) else out

def RequestTokens(chain_id):
    return False if (None == callRaw(f"rly testnets request {chain_id}",True)) else True

def RequestTokens_Process(chain_id, timeout, retry, delay):
    return False if (None == callTryRetry(f"rly testnets request {chain_id}", timeout, retry, delay,True)) else True

def TransferTokens(src_chain_id, dst_chain_id, amount, dst_chain_addr): # rly tx transfer hashquarkchain kira-1 1quark true $(rly ch addr kira-1)
    return False if (None == callRaw(f"rly tx transfer {src_chain_id} {dst_chain_id} {amount} true {dst_chain_addr}",True)) else True

def TryQueryBalance(chain_id):
    balance=callJson(f"rly q bal {chain_id} -j", False)
    return None if ((None != balance) and (len(balance) <= 0)) else balance

def DeletePath(path):
    return False if (None == callRaw(f"rly pth delete {path}",True)) else True

def GeneratePath(chain_id_src, chain_id_dst, path):
    out=callRaw(f"rly pth gen {chain_id_src} transfer {chain_id_dst} transfer {path}",True)
    return False if (None == out) else True

def QueryChainAddress(chain_id):
    out=callRaw(f"rly ch addr {chain_id}",True)
    return None if ((None != out) and len(out) <= 0) else out

def QueryPath(path):
    out=callJson(f"rly pth show {path} -j",True)
    return None if ((None != out) and len(out) <= 0) else out

def TransactClients(path):
    return False if (None == callRaw(f"rly transact clients {path}",True)) else True

def TransactConnection(path, timeout):
    return False if (None == callRaw(f"rly transact connection {path} --timeout {timeout}s",True)) else True

def TransactChannel(path, timeout):
    return False if (None == callRaw(f"rly transact channel {path} --timeout {timeout}s",True)) else True

def TransactLink(path, timeout):
    return False if (None == callRaw(f"rly transact link {path} --timeout {timeout}s",True)) else True

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

def KeyExists(chain_id, key_name): # rly keys show kira-alpha chain_key_kira-alpha
    out = callRaw(f"rly keys show {chain_id} {key_name}", False)
    return False if (None == out) else True

def ShowKey(chain_id, key_name): # rly keys show kira-1 chain_key_kira-1
    out = callRaw(f"rly keys show {chain_id} {key_name}", True)
    return None if (None == out) else out

# if key exists - deletes key, else returns true if key is already gone
def DeleteKey(chain_id, key_name): # rly keys delete kira-1 chain_key_kira-1
    if KeyExists(chain_id, key_name):
        return None != callRaw(f"rly keys delete {chain_id} {key_name}", True)
    else:
        return True

def RestoreKey(chain_id, key_name, mnemonic):
    return None if (None == callRaw(f"rly keys restore {chain_id} {key_name} '{mnemonic}'",True)) else True

def UpsertKey(chain_id, key_name):
    return callRaw(f"rly keys add {chain_id} {key_name}",True) # rly keys add kira-alpha chain_key_kira-alpha

def DownloadKey(bucket, s3_key_path, output_file):
    key_exists=callRaw(f"AWSHelper s3 object-exists --bucket='{bucket}' --path='{s3_key_path}' --throw-if-not-found=true",True)
    if None != key_exists:
        downloaded = callRaw(f"AWSHelper s3 download-object --bucket='{bucket}' --path='{s3_key_path}' --output={output_file}",True)
        if (None != downloaded) and os.path.isfile(output_file):
            return json.load(open(output_file))
    return { "mnemonic":None,"address":None }







