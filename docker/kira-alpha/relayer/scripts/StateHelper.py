import RelayerHelper
import ClientHelper
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



def DownloadKey(bucket, s3_key_path, output_file):
    key_exists=RelayerHelper.callRaw(f"AWSHelper s3 object-exists --bucket='{bucket}' --path='{s3_key_path}' --throw-if-not-found=true",True)
    if None != key_exists:
        downloaded = RelayerHelper.callRaw(f"AWSHelper s3 download-object --bucket='{bucket}' --path='{s3_key_path}' --output={output_file}",True)
        if (None != downloaded) and os.path.isfile(output_file):
            return json.load(open(output_file))
    return { "mnemonic":None,"address":None }

