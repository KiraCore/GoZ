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

# Update: (rm $SELF_SCRIPS/StateHelper.py || true) && nano $SELF_SCRIPS/StateHelper.py 
# Update: (rm $SELF_SCRIPTS/StateHelper.py || true) && nano $SELF_SCRIPTS/StateHelper.py 

def S3WriteText(text, bucket, s3_key_path):
    tmp_file=f"/tmp/{str(uuid.uuid4())}"
    StringHelper.WriteJsonToFile(text,tmp_file)
    print(f"INFO: Writing {tmp_file} to {bucket}/{s3_key_path} file in S3...")
    result = False if None == RelayerHelper.callRaw(f"AWSHelper s3 upload-object --bucket='{bucket}' --path='{s3_key_path}' --input='{tmp_file}'",True) else True
    if not result:
        print(f"ERROR: Failed to upload {tmp_file} into {bucket}/{s3_key_path} path on S3.")
    else: # remove tmp files only if success
        os.remove(tmp_file)
    return result

def S3FileExists(bucket, s3_key_path):
    return False if None == RelayerHelper.callRaw(f"AWSHelper s3 object-exists --bucket='{bucket}' --path='{s3_key_path}' --throw-if-not-found=True",True) else True

def S3ReadText(bucket, s3_key_path):
    tmp_file=f"/tmp/{str(uuid.uuid4())}"
    if not S3FileExists(bucket, s3_key_path):
        print(f"WARNING: File {bucket}/{s3_key_path} is not present in S3")
        return ""
    else:
        print(f"INFO: Found {bucket}/{s3_key_path} file in S3, reading...")

    downloaded = RelayerHelper.callRaw(f"AWSHelper s3 download-object --bucket='{bucket}' --path='{s3_key_path}' --output={tmp_file}",True)

    if None == downloaded:
        print(f"ERROR: Failed to read {s3_key_path} file from {bucket} bucket in S3")
        return None

    if not os.path.isfile(tmp_file):
        print(f"ERROR: Failed to read {bucket}/{s3_key_path} from the tmp directory {tmp_file}")
        return None

    file = open(tmp_file,mode='r')
    text_output = file.read()
    file.close()
    text_output = "" if not text_output else text_output
    print(f"SUCCESS: Read all {len(text_output)} characters from {bucket}/{s3_key_path} path in S3")
    return text_output


def DownloadKey(bucket, s3_key_path):
    text = S3ReadText(bucket, s3_key_path)
    return { "mnemonic":None, "address":None } if  not test else json.loads(text)