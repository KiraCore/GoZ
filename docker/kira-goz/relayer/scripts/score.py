import json
import requests
import time
import socket
import time
import datetime
import dateutil
import dateutil.parser
from datetime import datetime, timezone

print(f"GoZ Phase 1b scoreboard")

f = requests.get("https://goz.bitsong.network/api/clients?_limit=2000")
time_now = datetime.utcnow()
stats = json.loads(f.text)

game_start = dateutil.parser.isoparse("2020-05-18T07:00:00.000Z").replace(tzinfo=None)

eligiblePlayers=[]
for stat in stats:
    created_at=dateutil.parser.isoparse(stat["createdAt"]).replace(tzinfo=None)

    # player is out of the game if disconnected even once 
    # (because there already exist palyers with trust above 71h that are eligable to be scored)
    if created_at > game_start:
        continue

    # assume client updated at the beggining of the competition at least once
    updated_at=dateutil.parser.isoparse(stat.get("updatedAt", stat["createdAt"])).replace(tzinfo=None) 
    session_duration=(time_now - updated_at).total_seconds() # how much time passed since last update
    trusting = int(stat["trusting_period"][:-9]) # how ofthen the update must be made

    if trusting < session_duration: # player is out of the game if more time passed then trusting period
        continue

    eligiblePlayers.append(stat)

# sort players by trusting period
eligiblePlayers = sorted(eligiblePlayers, key=lambda k: int(k['trusting_period'][:-9])) 

# leaderboard should contain only unique competitors
position=0
distinctPlayers=[]
print(f"#TOP\t| CHAIN ID\t| TRUST PERIOD")
for player in eligiblePlayers:
    chain_id = player["chain_id"]
    if any(p["chain_id"] == chain_id for p in distinctPlayers):
        continue
    distinctPlayers.append(player)
    position = position + 1
    trusting = int(player["trusting_period"][:-9]) # how ofthen the update must be made
    print(f"#{position}\t| {chain_id}\t| {trusting}s")


    


#{
#    "_id":"5ec1920ea9e06596cd98f3f7",
#    "client_id":"qpndeinahkyh",
#    "chain_id":"snakey-1b",
#    "createdAt":"2020-05-15T12:19:59.180Z",
#    "last_height":"1294",
#    "signer":"cosmos1mvu547ythhm8c7ew2xnh6d8njhvdljgen3dr65",
#    "trusting_period":"511200000000000",
#    "unbonding_period":"1814400000000000",
#    "updatedAt":"2020-05-18T06:56:31.270Z",
#    "updates":13,
#    "id":"5ec1920ea9e06596cd98f3f7"
#}


