import StringHelper
import ArrayHelper
import subprocess
import json
import statistics
import multiprocessing
import sys
import time
from joblib import Parallel, delayed
from subprocess import Popen, PIPE

# runs utf-8 shell commands
def CMD(s):
    p = Popen(s, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True, encoding="utf-8")
    o, err = p.communicate()
    status = f"{p.wait()}"
    if status != "0":
        if len(status) < len(s)
           status=f"{status} => Command: {s}"
        if not err:
            raise Exception(f"Status: {status}")
        else:
            raise Exception(f"Status: {status} => Error: {StringHelper.Trim(str(err))}")
    if o == None:
        return ""
    return StringHelper.Trim(o)

    def IsString(s):
        return isinstance(data, (string))

def IsSafeJson(data):

def Process(func, args, q, showErrors):
    err = None
    try:
        o = func(*args)
        if q is not None:
            q.put({ "result": o, "failed": False, "error": None})
    except Exception as e:
        pass
        if q is not None:
            q.put({ "result": None, "failed": True, "error": e})

def TryRetryCMD(s, timeout, retry, delay, showErrors):
    return TryRetry(CMD, [ s ], timeout, retry, delay, showErrors)

# e.g. TryRetry(foo, [arg1, arg2, ... ], 60, 3, 0.1, True)
def TryRetry(func, args, timeout, retry, delay, showErrors):
    i = int(retry)
    while i >= 0:
        i = i - 1
        try:
            q = multiprocessing.Queue()
            mp = multiprocessing.Process(target = Process, args=(func, args, q, showErrors))
            mp.start()
            mp.join(timeout=timeout)
            alive = mp.is_alive()
            if not alive:
                result = q.get()
                failed = result["failed"]
                error = result["error"]
                result = result["result"]
                if failed:
                    raise error
                else:
                    return result
            else:
                mp.terminate()
                time.sleep(float(delay))
        except Exception as e:
            pass
            if showErrors:
                failures = (retry - i)
                print(f"ERROR({failures}/{retry}): {str(e)}")
            time.sleep(float(delay))
        if i <= 0:
            break
    return None