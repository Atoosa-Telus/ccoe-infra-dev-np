# [START imports]
import json
import sys
import os
import argparse
import datetime
import configparser
import yaml
from datetime import datetime
import sys
import argparse

sys.path.insert(0, './python-modules')
# sys.path.insert(0, './resources')
sys.dont_write_bytecode = True
# [END imports]

# [START import modules]
#import modules_config_handling as cf
import modules_bigquery_handling as bq
# [END import modules]

# [START] import google cloud modules
from google.cloud import bigquery
from google.cloud import storage
# [END] import google cloud modules

from resources.classes import ProjectClass
from resources.classes import RestfulClass

def import_config_yaml():
    with open("config.yaml", "r") as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
        return config

def import_restful_yaml():
    with open("restful.yaml", "r") as f:
        restful = yaml.load(f,Loader=yaml.FullLoader)
        return restful

# store data in a storage bucket and then write to BiGQuery --> need to add month partition later
if __name__ == "__main__":
    alias = ''

    for args in sys.argv:
        print(args)
        if args in ['logging', 'workbench']:
            alias = args

    if alias==True:
        os._exit(-1)

    config = import_config_yaml()

    project = ProjectClass(config['Project'], alias)
    valid_aliases = project.list_valid_aliases(config['Project'])
    print(valid_aliases)

    print(project.name)
    print(project.env)
    print(project)

    # bq.dataset_metadata_read()

