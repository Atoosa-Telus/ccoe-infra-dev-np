# [START imports]
import json
import sys
import os
import argparse
import datetime
from google.cloud import storage        # Import the Google Cloud client library 
import configparser
import pytz

utc=pytz.UTC
# [END imports]

def get_bucket_name():
    # get bucket name from config ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    bucket_name = config['BUCKET']['NAME']
   
    return bucket_name


def upload_blob_bucket(json_object, dest_blob_name):
    '''write json to bucket
    '''
    bucket_name = get_bucket_name()

    # Instantiates a client
    storage_client = storage.Client()
 
    # Get bucket name 
    bucket = storage_client.get_bucket(bucket_name)
 
    # declare json file name
    blob = bucket.blob(dest_blob_name)

    # upload json fiel as a blob in bucket
    blob.upload_from_string(
        data=json_object, 
        content_type='application/json'
        )

    # add error handling in here later    
    print("Json file: {} created in Bucket: {} ".format(blob.name, bucket.name))


def download_blob_bucket_as_json(file_name):
    '''get json from bucket
    '''
    bucket_name = get_bucket_name()

    # Automatically set credentials for bucket storage
    storage_client = storage.Client()

    # Get bucket name 
    bucket = storage_client.get_bucket(bucket_name)
 
     # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket)

    # Get the file I want, still do not knwo how
    blob = bucket.get_blob(file_name)
   
    # add error handling in here later    
    print("Reading json file: {}  from Bucket: {} ".format(blob.name, bucket.name))
    fileData = json.loads(blob.download_as_string(client=None))
    return fileData
