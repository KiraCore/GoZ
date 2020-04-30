import RelayerHelper
import FaucetHelper
import StringHelper
import ArrayHelper
import subprocess
import json
import statistics
import sys
import os
import os.path
import time
from joblib import Parallel, delayed


def Connect(chain_info_src, chain_info_dst):
    connection={}
    connection["src"]=chain_info_src
    connection["dst"]=chain_info_dst
    
    chain_id_src = chain_info_src["chain-id"]
    chain_id_dst = chain_info_src["chain-id"]
    path=f"{chain_id_src}_{chain_id_dst}"
    connection["path"]=path
    success = None
    path_info = None

    if (chain_id_src != chain_id_dst):
        RelayerHelper.DeletePath(path)
        success=RelayerHelper.GeneratePath(chain_id_src,chain_id_dst,path)
        path_info = None if (not success) else RelayerHelper.QueryPath(path)
    
    connection["info"] = path_info
    connection["success"] = (success and path_info and path_info["status"]["connection"])
    
    return connection