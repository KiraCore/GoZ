

import NetworkHelper
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

# python3 tcptest.py


#host="alpha.kiraex.com"
host="35.230.14.56"
#host="34.82.233.123"
#host="34.83.182.199"
#host="google.com"

print(f"Testing Host Ports: {host}...")

def TestPort(i):
    time.sleep(0.1)
    if NetworkHelper.IsPortOpen(host,i,3):
        print(f"Port {i} is OPEN")
        return i
    return None

result = Parallel(n_jobs=32)(delayed(TestPort)(i) for i in range(1,65536)) # min 1, max 65536

ports = [i for i in result if i] 
print(f"Finished Port Tester, host {host} has {len(result)} ports open:")
print(ports)
