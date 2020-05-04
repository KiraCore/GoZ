import json
import time
import sys
import os
import os.path


# Update: (rm $RELAY_SCRIPS/StringHelper.py || true) && nano $RELAY_SCRIPS/StringHelper.py 

def FixToAsciiN(s, c, N):
    asciiStr=(s.encode()[:N]).decode("ascii", "ignore")
    return asciiStr + (c * (N - len(asciiStr)))

# ref: https://docs.python.org/2.0/ref/strings.html
def Trim(s):
    if not s:
        return s
    oldLen = len(s)
    while True:
      s = s.strip(' ')
      s = s.strip('\n')
      s = s.strip('\r')
      s = s.strip('\t')
      s = s.strip('\a')
      s = s.strip('\a')
      s = s.strip('\b')
      s = s.strip('\f')
      s = s.strip('\v')
      newLen=len(s)
      if newLen == oldLen:
          return s
      else:
          oldLen = newLen
    
def IsString(s):
    return isinstance(s, (str))

def IsSafeJson(data):
    if data is None:
        return True
    elif isinstance(data, (bool, int, float)):
        return True
    elif isinstance(data, (tuple, list)):
        return all(IsSafeJson(x) for x in data)
    elif isinstance(data, dict):
        return all(isinstance(k, str) and IsSafeJson(v) for k, v in data.items())
    return False

def WriteToFile(s, path):
    f = open(path, "w")
    if not s:
        f.write("")
    else:
        if IsString(s):
            f.write(s)
        elif IsSafeJson(s):
            json.dump(s, f)
        else:
            f.write(str(s))
    f.close()
