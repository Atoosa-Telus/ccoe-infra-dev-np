# [START imports]
import json
import sys
import os
import argparse
import datetime
from google.cloud import storage        # Import the Google Cloud client library 
import configparser
import yaml
from datetime import datetime
import sys
import argparse

sys.dont_write_bytecode = True
# [END imports]

# [START import modules]
# import modules_storage_bucket as buck
import modules_database_bigquery as bq
# import modules_restful_statcanada as statcan
# [END import modules]

def read_bq_dataset_names():
    # get bigquery.client.dataset(dataset_id)
    dataset = bq.get_bigquery_dataset()


# store data in a storage bcuket and then write to BiGQuery --> need to add month partition later
if __name__ == "__main__":
    # get bigquery.client.dataset(dataset_id)
    read_bq_dataset_names()

