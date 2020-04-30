
import json
import time
import sys
import os
import os.path

def FixToAsciiN(s, c, N):
    asciiStr=(s.encode()[:N]).decode("ascii", "ignore")
    return asciiStr + (c * (N - len(asciiStr)))

def WriteToFile(s, path):
    file = open(path, "w") 
    file.write(s) 
    file.close()

