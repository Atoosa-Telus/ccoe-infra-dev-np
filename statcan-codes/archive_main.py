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
import modules_storage_bucket as buck
import modules_database_bigquery as bq
import modules_restful_statcanada as statcan
# [END import modules]

def statcan_data_to_storage():
    '''get current statcan data from Restful API calls and store json objects in buckets
    '''
    # get the series info & check if there was an error in api call
    try:
        seriesInfo = statcan.get_getSeriesInfo()
    except:
        # if ther is an error just print the error message
        print("There was an error in response to stat Canada, no response!")
        return

    # if there is no error uplpad the response content to bucket
    storage_file_name = get_storage_file_name('series_info')
    buck.upload_blob_bucket(seriesInfo, storage_file_name)
    
    # get the configuraion parmaeters form config.yaml   
    config_data = statcan.get_statcan_api_config()
    config_obj = config_data['STATCAN']['LATEST_N_PERIOD']

    # get payload for exchange rate , call api , get file_name, store in bucket
    payload = config_obj['EXCHANGE_RATE']
    latest_xch_rate = statcan.get_latestNperiod(payload)    
    storage_file_name = get_storage_file_name('exchange_rate')
    buck.upload_blob_bucket(latest_xch_rate, storage_file_name)

    # get payload for all CPI rates , call api , get file_name, store in bucket
    for cpi_ref_item in config_obj:
        if  ~(cpi_ref_item.find('CPI')):
            payload = config_obj[cpi_ref_item]
            cpi_latest = statcan.get_latestNperiod(payload)
            storage_file_name = get_storage_file_name(cpi_ref_item.lower())
            buck.upload_blob_bucket(cpi_latest, storage_file_name)


def create_bq_tables_if_not_exists():

    # get bigquery.client.dataset(dataset_id)
    dataset = bq.get_bigquery_dataset()
    
    # get the configuraion parmaeters form config.yaml   
    config_data = statcan.get_statcan_api_config()

    # check if there are any tables and only if not, then create
    # get series_info echema
    context = 'SERIES_INFO'
    schema_file = config_data['SCHEMA'][context]
    bq_tbl_name = config_data['BQ_TBLS'][context]
    #print("Checking if table '{}' exists".format(bq_tbl_name))
    if not (bq.find_dataset_table(dataset, bq_tbl_name)):
        print("creating table for '{}'".format(bq_tbl_name))
        bq.create_bigquery_table(schema_file, bq_tbl_name, dataset)

    # get exchange_rate echema
    context='EXCHANGE_RATE'
    schema_file = config_data['SCHEMA'][context]
    bq_tbl_name = config_data['BQ_TBLS'][context]
    #print("Checking if table '{}' exists".format(bq_tbl_name))
    if not (bq.find_dataset_table(dataset, bq_tbl_name)):
        print("creating table for '{}'".format(bq_tbl_name))
        bq.create_bigquery_table(schema_file, bq_tbl_name, dataset)

    # all cpi files hav esimilar schema
    context = 'CPI'
    schema_file = config_data['SCHEMA'][context]
    config_obj = config_data['STATCAN']['LATEST_N_PERIOD']
    for cpi_ref_item in config_obj:
        if  ~(cpi_ref_item.find(context)):
            bq_tbl_name = config_data['BQ_TBLS'][cpi_ref_item]
            #print("Checking if table '{}' exists".format(bq_tbl_name))
            if not (bq.find_dataset_table(dataset, bq_tbl_name)):
                print("creating table for '{}'".format(bq_tbl_name))
                bq.create_bigquery_table(schema_file, bq_tbl_name, dataset)

# TODO check if I need this at all
def get_storage_file_name(file_name):

    # construct full file name from the the file content reference
    storage_file_name = 'statcan_' + file_name.lower() + '.json'

    return storage_file_name

def load_bq_table_from_storage():
    # get bigquery.client.dataset(dataset_id)
    dataset = bq.get_bigquery_dataset()
    
    # get the configuraion parmaeters form config.yaml   
    config_data = statcan.get_statcan_api_config()

    # insert the data file as rows into bq
    context = 'SERIES_INFO'
    schema_file = config_data['SCHEMA'][context]
    bq_tbl_name = config_data['BQ_TBLS'][context]
    data_file = get_storage_file_name(context)
    bq.insert_rows_bigquery_table(schema_file, data_file, bq_tbl_name, dataset)

    # insert the data file as rows into bq
    context = 'EXCHANGE_RATE'
    schema_file = config_data['SCHEMA'][context]
    bq_tbl_name = config_data['BQ_TBLS'][context]
    data_file = get_storage_file_name(context)
    bq.insert_rows_bigquery_table(schema_file, data_file, bq_tbl_name, dataset)

       
    # insert the data file as rows into bq
    context = 'CPI'
    schema_file = config_data['SCHEMA'][context]
    config_obj = config_data['STATCAN']['LATEST_N_PERIOD']
    for cpi_ref_item in config_obj:
        if  ~(cpi_ref_item.find(context)):
            bq_tbl_name = config_data['BQ_TBLS'][cpi_ref_item]
            data_file = get_storage_file_name(cpi_ref_item)
            bq.insert_rows_bigquery_table(schema_file, data_file, bq_tbl_name, dataset)
    

def update_bq_table_add_rows():
    # get bigquery.client.dataset(dataset_id)
    dataset = bq.get_bigquery_dataset()

    # get the configuraion parmaeters form config.yaml   
    config_data = statcan.get_statcan_api_config()
    config_obj = config_data['STATCAN']['LATEST_ONE']

    # check if there is any update in statcan data
    context = 'EXCHANGE_RATE'
    payload = config_obj[context]
    api_latest_data = json.loads(statcan.get_latestNperiod(payload))
    schema_file = config_data['SCHEMA'][context]
    bq_tbl_name = config_data['BQ_TBLS'][context]
    bq.insert_row_if_new(api_latest_data, schema_file, bq_tbl_name, dataset)
      
    # insert the data file as rows into bq
    context = 'CPI'
    schema_file = config_data['SCHEMA'][context]
    for cpi_ref_item in config_obj:
        if  ~(cpi_ref_item.find(context)):
            payload = config_obj[cpi_ref_item]
            api_latest_data = json.loads(statcan.get_latestNperiod(payload))
            bq_tbl_name = config_data['BQ_TBLS'][cpi_ref_item]
            bq.insert_row_if_new(api_latest_data, schema_file, bq_tbl_name, dataset)

def delete_tables_excl_series_info():
    # get bigquery.client.dataset(dataset_id)
    dataset = bq.get_bigquery_dataset()

    # get the configuraion parmaeters form config.yaml   
    config_data = statcan.get_statcan_api_config()
    config_obj = config_data['STATCAN']['LATEST_ONE']

    # series_info table need not ever be modified, updated or deleted 
    context = 'SERIES_INFO'
    bq_tbl_name = config_data['BQ_TBLS'][context]
    bq.delete_table_if_exists(bq_tbl_name, dataset)
    
    # get the table_name for deletion
    context = 'EXCHANGE_RATE'
    bq_tbl_name = config_data['BQ_TBLS'][context]
    bq.delete_table_if_exists(bq_tbl_name, dataset)

    # get the table_name for deletion
    context = 'CPI'
    for cpi_ref_item in config_obj:
        if  ~(cpi_ref_item.find(context)):
            bq_tbl_name = config_data['BQ_TBLS'][cpi_ref_item]
            bq.delete_table_if_exists(bq_tbl_name, dataset)


def create_views_for_visualization():
    
    # cross joi, aggreagate and colnstruct a view tabel ready for Tableau
    bq.create_view_tables()

    #I need to create a json file of tables, columen names and joint condition 

# store data in a storage bcuket and then write to BiGQuery --> need to add month partition later
if __name__ == "__main__":
    # get current statcan data from Restful API calls and store json objects in buckets
    #statcan_data_to_storage()

    # check if the tables exist, do it one by one and create with prfixe schema if they dont' exist
    #create_bq_tables_if_not_exists()

    # not to be used in production, just to be used during development
    #delete_tables_excl_series_info()

    # get statcan stored data from bcukets and insert the data file as rows into bq
    #load_bq_table_from_storage()
    
    # get one row for wach endpoitna nd check if it  new then iknsert into bigquery tables
    update_bq_table_add_rows()

    # add views needed for Visualization dashboard
    #create_views_for_visualization()


