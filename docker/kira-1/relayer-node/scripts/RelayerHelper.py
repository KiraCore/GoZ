
from subprocess import Popen, PIPE
import json
import statistics
import multiprocessing
import time

# python3 -m pip install joblib
# python3 -m pip install multiprocessing

def callRaw(s, showErrors):
    try:
        p = Popen(s, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        o = p.stdout.readline().strip()
        err = p.stderr.readline().strip()
        return o
    except Exception as e:
        pass
        if showErrors:
            if err is not None:
                print("Call failed with error: '" + str(err) + "'.")
            else:
                print("Call failed during output parsing: '" + str(e) + "'.")
        return None

def callRawTrue(s, showErrors):
    try:
        p = Popen(s, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        o = p.stdout.readline().strip()
        err = p.stderr.readline().strip()
        if not not err:
            print("Call ended with error: '" + str(err) + "'.")
            return None
        if not err and not o:
            return True
        return o
    except Exception as e:
        pass
        if showErrors:
            if err is not None:
                print("Call failed with error: '" + str(err) + "'.")
            else:
                print("Call failed during output parsing: '" + str(e) + "'.")
        return None

def call(s,q, showErrors):
    try:
        p = Popen(s, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        o = p.stdout.readline().strip()
        err = p.stderr.readline().strip()
        j = json.loads(o)
        if q is not None:
            q.put(j)
        time.sleep(1) # rate limiting protection
        return j
    except Exception as e:
        pass
        time.sleep(1) # rate limiting protection
        if showErrors:
            if err is not None:
                print("Call failed with error: '" + str(err) + "'.")
            else:
                print("Call failed during output parsing: '" + str(e) + "'.")
        if q is not None:
            q.put(None)
        return None

def callRetry(s, timeout, retry, delay, showErrors):
    i = retry
    result = None
    while i >= 0 and (result is None):
        i = i - 1
        try:
            mq = multiprocessing.Queue()
            mp = multiprocessing.Process(target = call, args=(s,mq,showErrors,))
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

def rly(s):
    s = str(s).lstrip()
    return call("rly " + s, None, True)


