
import IBCHelper
import RelayerHelper
import StringHelper
import StateHelper
import ClientHelper
import NetworkHelper
import TaskHelper
import ArrayHelper
import subprocess
import json
import statistics
import sys
import os
import time
import dateutil.parser
from datetime import datetime, timezone
from joblib import Parallel, delayed


# Update: (rm $SELF_SCRIPTS/test.py || true) && nano $SELF_SCRIPTS/test.py 


print(dateutil.__version__)

print("Test Script Start")

test={"a":1}
test["a"] = z = 4
print(f"Ok: {test}, {z}")

d1=datetime.utcnow()
d2=dateutil.parser.isoparse('2020-05-08T16:38:40.583380838Z').replace(tzinfo=None)
dt=d1-d2
print(int(dt.total_seconds()))
'''
connection={
   "src": { "chain-id":"kira-alpha" },
   "dst": { "chain-id":"kira-1" },
   "path": "kira-alpha_kira-1",
   "path-info": {"chains":{
      "src":{"chain-id":"kira-alpha","client-id":"ubohltylat","connection-id":"tdeeqbwuau","channel-id":"ejjggqwtkm","port-id":"transfer","order":"ORDERED"},
      "dst":{"chain-id":"kira-1","client-id":"mbxdppcthy","connection-id":"wqvfpxjmzy","channel-id":"qzjrrvnwzn","port-id":"transfer","order":"ORDERED"},
      "strategy":{"type":"naive"}},
      "status":{"chains":true,"clients":true,"connection":true,"channel":true}
      }
}
print(RelayerHelper.AddPath(connection))
'''

print("Test Script End")

{"client_state":{
   "type":"ibc/client/tendermint/ClientState",
   "value":{
      "id":"hbgslzbmam","trusting_period":"600000000000","unbonding_period":"1814400000000000","MaxClockDrift":"10000000000","frozen_height":"0","last_header":{"SignedHeader":{"header":{"version":{"block":"10","app":"0"},"chain_id":"kira-1","height":"41527","time":"2020-05-08T16:38:40.583380838Z","last_block_id":{"hash":"F96F418BEB24B585E1ADE3FA56D18314EA590B9491F7D62C28011FB8E66C6D42","parts":{"total":"1","hash":"F1A40C498004064893E437071FD1BD982A5837CEA5A101363E5447D53118E904"}},"last_commit_hash":"894650C5BDF78716327B33D03A757A3584567F1FBAFDD5D2E29773E34A0EDCFA","data_hash":"","validators_hash":"EBA90C3774DCB47ACA614C615FCCADD10AFE8B7398781D1FFB8EE1C18BBED710","next_validators_hash":"EBA90C3774DCB47ACA614C615FCCADD10AFE8B7398781D1FFB8EE1C18BBED710","consensus_hash":"048091BC7DDC283F77BFBF91D73C44DA58C3DF8A9CBC867405D8B7F3DAADA22F","app_hash":"6929A1D54D87722145E9CA3623407197C020283739124CDFD94CD0078F9CF495","last_results_hash":"6E340B9CFFB37A989CA544E6BB780A2C78901D3FB33738768511A30617AFA01D","evidence_hash":"","proposer_address":"8AE1ED081992EBE409056DC023629023A6511007"},"commit":{"height":"41527","round":"0","block_id":{"hash":"839390AF81DDB7F1AF329FE06C3544910CCD4C260C5C3C19FA07BB50BBBEC984","parts":{"total":"1","hash":"84F24FD445988CAA7B7632B200B5045980BDF681C7B4C7A50AC17E9936DC2026"}},"signatures":[{"block_id_flag":2,"validator_address":"8AE1ED081992EBE409056DC023629023A6511007","timestamp":"2020-05-08T16:38:45.607240893Z","signature":"G2W6L3fztHwPKSEN7JodIZiXqYWbYBQY9FR6r3GcKX8omvs36KINDJflnEdaZ5pMu1hT0Z/BmUmnxfD+0vJFCg=="}]}},"validator_set":{"validators":[{"address":"8AE1ED081992EBE409056DC023629023A6511007","pub_key":{"type":"tendermint/PubKeyEd25519","value":"EEKSA1W83OA2C94ZEiJOMi2Z6ql+Yq03KsvkH4gaEns="},"voting_power":"90000","proposer_priority":"0"}],"proposer":{"address":"8AE1ED081992EBE409056DC023629023A6511007","pub_key":{"type":"tendermint/PubKeyEd25519","value":"EEKSA1W83OA2C94ZEiJOMi2Z6ql+Yq03KsvkH4gaEns="},"voting_power":"90000","proposer_priority":"0"}}}}},"proof":{"proof":{"ops":[{"type":"iavl:v","key":"Y2xpZW50cy9oYmdzbHpibWFtL2NsaWVudFN0YXRl","data":"qwMKqAMKKggQEHkY0MMCKiB1kdnLWo/llvvJWjXY33y0tnPynHcZkvlQcJag5noiPwoqCA4QMBjQwwIiIMTjPiL7LVJG4P/YjGUj/CIsuLcOJCia/gyyRdQZcmUkCioIDBAfGNDDAiogYv3QFh34Xtyypc94JNhh5feymWfOfaAdXyOPPNgJ/7kKKggKEBEY0MMCIiA9Jyys4m/KjPUdDVsIc2dB/XjCzcuPh9unJeXdHPyOtAoqCAgQCxjQwwIqIJ2NAQofZ1vM3SmzirtQ3TmONORFIxe5QbvcwZjY16ryCioIBhAIGNDDAiogomO/MqMBcJJzcBMwBPinMcfi8mC6x8m+MIiN1fsu/x0KKggEEAQY0MMCIiAhqe8wXrmbTYlFiVuyi9uckgRhxQ+5N5RUPx4dz4kmdwoqCAIQAhjQwwIqIEY1SIf20f80tKcNzcQXvkBpNxlxK4SJ/dLpld+xOKAmGkYKHmNsaWVudHMvaGJnc2x6Ym1hbS9jbGllbnRTdGF0ZRIgANEVjr/5h0di/8WvS84Z7Lqq4QbCgC0kOWAs2Lxb5aMY0MMC"},{"type":"multistore","key":"aWJj","data":"CvcECi8KA2FjYxIoCiYImsQCEiBdm2jkXE90Ngj/NVzOXL70VZo93SsTTaoi6Fvy8nPkSQovCgNnb3YSKAomCJrEAhIgYM0TfBli7KxhY4nWgDSDPykhUJwtKFql9RU5l86WinQKLwoDaWJjEigKJgiaxAISIDAumFWqRrnmyR8bqvV2PUHffW5okaBPc/RpaXxJUtVHCjYKCmNhcGFiaWxpdHkSKAomCJrEAhIgHblaRyOVG2FJ83gNMaZEN0Ont++VsllVOraVCb887ZMKEgoIZXZpZGVuY2USBgoECJrEAgo0CghzbGFzaGluZxIoCiYImsQCEiBtfBA9xhuxvmYrOjhf2+2vnkvmJJKIQMhMzUhOOHoU6wowCgRiYW5rEigKJgiaxAISIO0cJr+NuPXHGogTcCw5U0xwjiyx09Z4LW8i+wsf3wy5ChEKB3VwZ3JhZGUSBgoECJrEAgoQCg5tZW1fY2FwYWJpbGl0eQo0Cgh0cmFuc2ZlchIoCiYImsQCEiCtdxLMpRJ0Aom3FLEbmPPES9H/JukxNJ0t6SoQH+KRBwowCgRtaW50EigKJgiaxAISIPNxpFmQf6nsHoRLS4ER5ElKrw2wV/8bFgMUQ971WSOyCjgKDGRpc3RyaWJ1dGlvbhIoCiYImsQCEiBF5Q1G8/Q2I1KmOWhsJK4qAPGVMpvHbWIiVWwNgEPcTwoyCgZwYXJhbXMSKAomCJrEAhIglFom9eN9gQuPzK5aCvXhE8taX1JbDzm86VP7yIWnfS0KMwoHc3Rha2luZxIoCiYImsQCEiCIPO1ITJbZ8WBlwA87wjAF0chrr55Ok2XxL7QySrhaxA=="}]}},"proof_path":{"key_path":[{},{}]},"proof_height":"41498"}