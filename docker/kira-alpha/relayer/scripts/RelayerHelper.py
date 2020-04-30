import FaucetHelper
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

def callRawTrue(s, showErrors):
    try:
        p = Popen(s, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        o, err = p.communicate()
        if not not err:
            print(f"Call '{s}' ended with error: {str(err)}")
            return None
        if not err and not o:
            return True
        return o
    except Exception as e:
        pass
        if showErrors:
            if err is not None:
                print(f"Call '{s}' failed with error: {str(err)}")
            else:
                print(f"Call '{s}' failed during output parsing: {str(err)}")
        return None

def callJson(s, showErrors):
    try:
        p = Popen(s, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        o, err = p.communicate()
        if (not (not err)):
            print(f"Call '{s}' ended with error: {str(err)}")
            return None
        if (not err) and (not o):
            return {}
        return json.loads(o)
    except Exception as e:
        pass
        if showErrors:
            if err is not None:
                print(f"Call '{s}' failed with error: {str(err)}")
            else:
                print(f"Call '{s}' failed to parse output: '{str(o)}', error: {str(err)}")
        return None

def callProcessRawTrue(s, q, showErrors):
    try:
        p = Popen(s, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        o, err = p.communicate()
        if not not err:
            print(f"Call '{s}' ended with error: {str(err)}")
            o = None
        if not err and not o:
            o = True
        if q is not None:
            q.put(o)
        time.sleep(1) # rate limiting protection
        return o
    except Exception as e:
        pass
        if showErrors:
            if err is not None:
                print(f"Call '{s}' failed with error: {str(err)}")
            else:
                print(f"Call '{s}' failed during output parsing: {str(err)}")
        if q is not None:
            q.put(o)
        return None

def callRetryTrue(s, timeout, retry, delay, showErrors):
    i = retry
    result = None
    while i >= 0 and (result is None):
        i = i - 1
        try:
            mq = multiprocessing.Queue()
            mp = multiprocessing.Process(target = callProcessRawTrue, args=(s,mq,showErrors,))
            mp.start()
            mp.join(timeout=timeout)
            alive = mp.is_alive()
            if not alive:
                result = mq.get()
            else:
                mp.terminate()
        except:
            pass
        if result is None:
            time.sleep(int(delay))
        else:
            break 

    return result

def ConfigureDefaultKey(chain_id, key_name):
    return False if (not callRawTrue(f"rly ch edit {chain_id} key {key_name}",True)) else True

def ChainDelete(chain_id):
    return False if (not callRawTrue(f"rly chains delete {chain_id}",True)) else True

def AddChainFromFile(chain_info_path):
    return False if (not callRawTrue(f"rly ch add -f {chain_info_path}",True)) else True

def DeleteLiteClient(chain_id):
    return False if (not callRawTrue(f"rly lite delete {chain_id}",True)) else True

def InitLiteClient(chain_id):
    return False if (not callRawTrue(f"rly lite init {chain_id} -f",True)) else True

def InitLiteClient_Process(chain_id, timeout, retry, delay):
    return False if (not callRetryTrue(f"rly lite init {chain_id} -f",timeout,retry,delay,True)) else True

def UpdateLiteClient(chain_id):
    return False if (not callRawTrue(f"rly lite update {chain_id}",True)) else True

def UpdateLiteClient_Process(chain_id, timeout, retry, delay):
    return False if (not callRetryTrue(f"rly lite update {chain_id}",timeout,retry,delay,True)) else True

def QueryLiteClientHeader(chain_id):
    header=callJson(f"rly lite header {chain_id}",True)
    return None if (not header) else header

def RequestTokens(chain_id):
    return False if (not callRawTrue(f"rly testnets request {chain_id}",True)) else True

def RequestTokens_Process(chain_id, timeout, retry, delay):
    return False if (not callRetryTrue(f"rly testnets request {chain_id}", timeout, retry, delay,True)) else True

def TransferTokens(src_chain_id, dst_chain_id, amount, dst_chain_addr): # rly tx transfer hashquarkchain kira-1 1quark true $(rly ch addr kira-1)
    return False if (not callRawTrue(f"rly tx transfer {src_chain_id} {dst_chain_id} {amount} true {dst_chain_addr}",True)) else True

def QueryBalance(chain_id):
    balance=callRawTrue(f"rly q bal {chain_id} -j",True)
    return None if (not balance) else json.loads(balance)

def DeletePath(path):
    return False if (not callRawTrue(f"rly pth delete {path}",True)) else True

def GeneratePath(chain_id_src, chain_id_dst, path):
    out=callRawTrue(f"rly pth gen '{chain_id_src}' transfer '{chain_id_dst}' transfer '{path}'",True)
    return False if (not out) else True

def QueryChainAddress(chain_id):
    addr=callRawTrue(f"rly ch addr {chain_id}",True)
    return None if (not addr) else addr

def QueryPath(path):
    out=callRawTrue(f"rly pth show {path} -j",True)
    return None if (not out) else out

def GetAmountByDenom(balances, denom):
    amount = 0
    if balances and (len(balances) > 0):
        for balance in balances:
            if (not balance) or (balance["denom"] != denom):
                continue
            else:
                amount = int(balance["amount"])
    return amount

def DeleteKey(chain_id, key_name):
    return False if (not callRawTrue(f"rly keys delete '{chain_id}' '{key_name}'",False)) else True

def RestoreKey(chain_id, key_name, mnemonic):
    return None if (not callRawTrue(f"rly keys restore '{chain_id}' '{key_name}' '{mnemonic}'",True)) else True

def UpsertKey(chain_id, key_name):
    return callRawTrue(f"rly keys add '{chain_id}' '{key_name}'",True)

def DownloadKey(bucket, s3_key_path, output_file):
    key_exists=callRawTrue(f"AWSHelper s3 object-exists --bucket='{bucket}' --path='{s3_key_path}' --throw-if-not-found=true",True)
    if key_exists:
        downloaded = callRawTrue(f"AWSHelper s3 download-object --bucket='{bucket}' --path='{s3_key_path}' --output={output_file}",True)
        if downloaded and os.path.isfile(output_file):
            return json.load(open(output_file))
    return { "mnemonic":None,"address":None }







