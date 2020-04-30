import StringHelper
import ArrayHelper
import subprocess
import json
import statistics
import sys
import os
import time
from joblib import Parallel, delayed
import socket

def IsPortOpen(host,port,timeout):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host,port))
        return (result == 0)
    except:
        return False
    finally:
        # s.shutdown(socket.SHUT_RDWR)
        time.sleep(0.1)
        s.close()


