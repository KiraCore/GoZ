

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


host="google.com"
#host="35.230.14.56"
#host="34.82.233.123"
#host="34.83.182.199"
#host="google.com"

print(f"Testing Host Ports: {host}...")

last_open=False
def TestPort(i):
    global last_open
    if NetworkHelper.IsPortOpen(host,i,2):
        print(f"Port {i} is OPEN       ")
        last_open = True
        return i
    else:
        if last_open:
            print(f"Port {i} is CLOSED")
        else:
            print(f"Port {i} is CLOSED\r",end="")
        last_open = False
        return None


for p in range(1,65536):
    TestPort(p)

print(f"Finished Testing {host}")
#print(f"Finished Port Tester, host {host} has {len(result)} ports open:")
#print(ports)

