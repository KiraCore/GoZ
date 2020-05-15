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
import uuid

# Update: (rm $SELF_SCRIPTS/StateHelper.py || true) && nano $SELF_SCRIPTS/StateHelper.py 
def S3WriteText(text, bucket, s3_key_path):
    tmp_file=f"/tmp/{str(uuid.uuid4())}"
    StringHelper.WriteJsonToFile(text,tmp_file)
    print(f"INFO: Writing {tmp_file} to {bucket}/{s3_key_path} file in S3...")
    result = RelayerHelper.callRaw(f"AWSHelper s3 upload-object --bucket='{bucket}' --path='{s3_key_path}' --input='{tmp_file}'",True)
    os.remove(tmp_file)
    if result == None:
        raise Exception(f"ERROR: Failed to upload {tmp_file} into {bucket}/{s3_key_path} path on S3.")
    return True

def TryS3WriteText(text, bucket, s3_key_path):
    try:
        return S3WriteText(text, bucket, s3_key_path)
    except Exception as e:
        pass
        print(f"ERROR: S3 Write => {str(e)}")
        return None

def TryS3FileExists(bucket, s3_key_path):
    return False if None == RelayerHelper.callRaw(f"AWSHelper s3 object-exists --bucket='{bucket}' --path='{s3_key_path}' --throw-if-not-found=True",False) else True

def S3FileExists(bucket, s3_key_path):
    out = RelayerHelper.callRaw(f"AWSHelper s3 object-exists --bucket='{bucket}' --path='{s3_key_path}' --throw-if-not-found=False --silent=True",True)
    if None == out:
        raise Exception(f"Call failed when checking if file exists as {s3_key_path} in the {bucket} S3 bucket")
    return StringHelper.ToBool(out)

def S3ReadText(bucket, s3_key_path):
    if not S3FileExists(bucket, s3_key_path):
        print(f"WARNING: File {bucket}/{s3_key_path} does not exist in S3")
        return {}
        
    out = RelayerHelper.callRaw(f"AWSHelper s3 download-text --bucket='{bucket}' --path='{s3_key_path}' --silent=true --throw-if-not-found=False",True)
    if None == out:
        raise Exception(f"Failed to read {s3_key_path} file from {bucket} bucket in S3")
    else:
        print(f"SUCCESS: Read all {len(out)} characters from {bucket}/{s3_key_path} path in S3")
        return out

def S3ReadJson(bucket, s3_key_path): # AWSHelper s3 object-exists --bucket='kira-core-goz' --path='relayer/kira-alpha_kira-1-1b/alpha/state.json' --throw-if-not-found=False
    if not S3FileExists(bucket, s3_key_path):
        print(f"WARNING: File {bucket}/{s3_key_path} does not exist in S3")
        return {}

    out = RelayerHelper.callJson(f"AWSHelper s3 download-text --bucket='{bucket}' --path='{s3_key_path}' --silent=true --throw-if-not-found=False",True)
    if None == out:
        raise Exception(f"Failed to read {s3_key_path} file from {bucket} bucket in S3")
    else:
        print(f"SUCCESS: Read all {len(out)} json elements from {bucket}/{s3_key_path} path in S3")
        return out

def TryS3ReadText(bucket, s3_key_path):
    out = RelayerHelper.callRaw(f"AWSHelper s3 download-text --bucket='{bucket}' --path='{s3_key_path}' --silent=true",True)
    if None == out:
        print(f"ERROR: Failed to read {s3_key_path} file from {bucket} bucket in S3")
    else:
        print(f"SUCCESS: Read all {len(out)} characters from {bucket}/{s3_key_path} path in S3")
    return out

def DownloadKey(bucket, s3_key_path):
    text = S3ReadText(bucket, s3_key_path)
    return { "mnemonic":None, "address":None } if not test else json.loads(text)