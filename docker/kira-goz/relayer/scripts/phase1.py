
import IBCHelper
import RelayerHelper
import FaucetHelper
import StringHelper
import ArrayHelper
import subprocess
import json
import statistics
import sys
import os
import time
from joblib import Parallel, delayed


# Startup example: 26657
# python3 $RELAY_SCRIPS/phase1.py "$TESTCHAIN_JSON_PATH" "$RLYKEY_MNEMONIC" "$GOZCHAIN_JSON_PATH" "$RLYKEY_MNEMONIC" $BUCKET
# python3 $RELAY_SCRIPS/phase1.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $HUBCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $BUCKET

# console args
SRC_JSON_DIR=sys.argv[1]
SRC_MNEMONIC=sys.argv[2]
DST_JSON_DIR=sys.argv[3]
DST_MNEMONIC=sys.argv[4]
BUCKET=sys.argv[5]

# constants 
connect_timeout = 60

connection = IBCHelper.ConnectWithJson(SRC_JSON_DIR, SRC_MNEMONIC, DST_JSON_DIR, DST_MNEMONIC, BUCKET, connect_timeout)
connected = False if (not connection) else connection["success"]
path = None if (not connection) else connection["path"]

if (not connected):
   print(f"Failed to establish connection using {SRC_JSON_DIR} and {DST_JSON_DIR}")
   exit(1)

src_chain_info = connection["src"]
dst_chain_info = connection["dst"]
src_id = src_chain_info["chain-id"]
dst_id = dst_chain_info["chain-id"]
src_balance = src_chain_info["balance"]
dst_balance = src_chain_info["balance"]

print(f"Success connection between {src_id} and {dst_id} was established, path: '{path}'")


#if(len(src_balance) <= 0) and (len(src_balance) < 0)

#RelayerHelper.TransferTokens(src_chain_id, dst_chain_id, amount, dst_chain_addr)

# rly pth delete kira-alpha_hashquarkchain
    # rly pth gen kira-alpha transfer hashquarkchain transfer kira-alpha_hashquarkchain
    # rly transact link kira-alpha_kira-1
    # rly transact clients kira-alpha_kira-1 --debug # clients connect
    # rly transact connection kira-alpha_kira-1 --debug # clients connection
    # rly transact channel kira-alpha_kira-1 --debug # channel connect

# rly pth delete kira-alpha_hashquarkchain
# rly pth gen kira-alpha transfer hashquarkchain transfer kira-alpha_hashquarkchain
# rly transact link kira-alpha_hashquarkchain --debug
# rly transact clients kira-alpha_hashquarkchain --debug # clients connect
# rly transact connection kira-alpha_hashquarkchain --debug # clients connection
# rly transact channel kira-alpha_hashquarkchain --debug # channel connect


# rly pth delete kira-alpha_hashquarkchain
# rly pth gen kira-alpha transfer hashquarkchain transfer kira-alpha_hashquarkchain
# rly transact clients kira-alpha_hashquarkchain --debug # clients connect
# rly transact connection kira-alpha_hashquarkchain --debug # clients connection
# rly transact channel kira-alpha_hashquarkchain --debug # channel connect
# rly transact link kira-alpha_hashquarkchain --debug

# rly transact channel-close kira-alpha_hashquarkchain
# rly tx channel-close kira-alpha_hashquarkchain --timeout 10s



#status = None if (not path_info) else path_info["status"]
#connected = None if (not status) else (status["chains"] and status["clients"] and status["connection"] and status["channel"])


# rly transact connection kira-alpha_kava-ibc
# rly pth show kira-alpha_kava-ibc

# rly transact channel-close kira-alpha_nibiru-ibc
# rly pth delete kira-alpha_nibiru-ibc
# rly pth gen kira-alpha transfer nibiru-ibc transfer kira-alpha_nibiru-ibc
# rly transact link kira-alpha_nibiru-ibc --debug
# rly transact channel kira-alpha_nibiru-ibc --debug 



######################################### rly paths add kira-1 hashquarkchain kira-1_hashquarkchain
### rly pth gen kira-1 transfer hashquarkchain transfer kira-1_hashquarkchain
## rly tx link kira-1_hashquarkchain
#
## rly q bal kira-1 -j
## rly q bal hashquarkchain -j
#
##rly ch addr hashquarkchain
#
## rly tx transfer hashquarkchain kira-1 1quark true $(rly ch addr kira-1)
## rly tx transfer kira-1 hashquarkchain 1ukex true $(rly ch addr hashquarkchain)