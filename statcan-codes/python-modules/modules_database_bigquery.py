# [START imports]
import json
import sys
import os
import argparse
import datetime
from google.cloud import storage        # Import the Google Cloud client library 
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import configparser
import pytz
import io

utc=pytz.UTC
# [END imports]

# [START import modules]
# import modules_storage_bucket as buck
# import modules_database_bigquery as bq
# import modules_restful_statcanada as statcan
# [END import modules]

def get_dataset_name():

    # get dataset name from config ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    dataset_id = config['DATASET']['NAME']
 
    return dataset_id

def find_dataset_table(dataset,table_name):

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # check if there are any tables in this dataset
    tables = list(client.list_tables(dataset))  # Make an API request(s).
    if tables:
        for table in tables:
                if str(table.table_id).lower() == str(table_name).lower():
                    print("Table '{}' exists!".format(table_name))
                    return True
    return False

def get_bigquery_dataset():

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # call ge_datset from bq module to get the datset from config file
    dataset_id = get_dataset_name()

    # get dataset object from bigquery client with dataset names
    dataset = client.get_dataset(str(dataset_id))  # Make a API request.

    return dataset

def create_bigquery_table(schema_file, table_name, dataset):

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # concat project naame and dataset name and table name for table_id
    table_id = dataset.project + '.' + dataset.dataset_id + '.' + str(table_name)
      
    # laod json schema object rom storage
    schema = buck.download_blob_bucket_as_json(schema_file)

    # create table from manually generated schema file
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))


def insert_rows_bigquery_table(schema_file, data_file, table_name, dataset):

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # get dataset object from bigquery client with dataset names
    dataset = get_bigquery_dataset()

    # concat project naame and dataset name and table name for table_id
    table_id = dataset.project + '.' + dataset.dataset_id + '.' + table_name

    # laod json schema object from storage
    schema = buck.download_blob_bucket_as_json(schema_file)

    # laod json data object from storage
    data = buck.download_blob_bucket_as_json(data_file)
    
    # convert json to rows of json data
    rows_to_insert = [data]

    errors = client.insert_rows_json(
        table_id, rows_to_insert, row_ids=[None] * len(rows_to_insert)
    )  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


def query_latest_datapoint_in_table(sql_script):

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # Run a SQL script.
    query_job = client.query(sql_script)

    # Wait for the whole script to finish.
    rows_iterable = query_job.result()
    print("Script created {} child jobs.".format(query_job.num_child_jobs))

    # Fetch result rows for the final sub-job in the script.
    rows = list(rows_iterable)
    print("{} of the most recent data points.".format(len(rows)))
 
    return query_job
    

def check_if_table_uptodate(api_data, schema_file, table_id, dataset):

    # construct a wuery script to read lates row ordered by ref period date
    query_script_base = """SELECT
            v.refPer as ref_period, 
            FROM `{}` AS r, 
            UNNEST(r.vectorDataPoint) AS v
            ORDER BY ref_period DESC
            LIMIT 1;
            """        
    query_script = query_script_base.format(table_id)

    # run the query against the bigquery
    query_data = query_latest_datapoint_in_table(query_script)
    print("statcan latest data refPeriod={}".format(api_data['vectorDataPoint'][0]['refPer']))
    
    for query_row in query_data:
        # Row values can be accessed by field name or index
        print("refPeriod={}".format(query_row['ref_period']))
        if str(query_row.ref_period) == str(api_data['vectorDataPoint'][0]['refPer']):
            print("it simply matches!!!!")
            return True

    return True


def insert_row_if_new(api_data, schema_file, table_name, dataset):

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # concat project naame and dataset name and table name for table_id
    table_id = dataset.project + '.' + dataset.dataset_id + '.' + table_name

    # convert json to rows of json data
    rows_to_insert = [api_data]

    if check_if_table_uptodate(api_data, schema_file, table_id, dataset):
        print("The table is up-to-date, no ction to be done | Good to continue!")
        return

    errors = client.insert_rows_json(
        table_id, rows_to_insert, row_ids=[None] * len(rows_to_insert)
    )  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))
    


def delete_table_if_exists(table_name, dataset):

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # concat project naame and dataset name and table name for table_id
    table_id = dataset.project + '.' + dataset.dataset_id + '.' + table_name

    client.delete_table(table_id, not_found_ok=True)  # Make an API request.
    print("Deleted table '{}'.".format(table_id))


def create_view_tables():

    # Construct a BigQuery client object.
    client = bigquery.Client()

    join_query_file = open('statcan_bq_join_query.sql','r')
    sql_join_script=str(join_query_file.read())
    join_query_file.close()
    # Run a SQL script.
    query_job = client.query(sql_join_script)

    # Wait for the whole script to finish.
    rows_iterable = query_job.result()
    print("Script created {} child jobs.".format(query_job.num_child_jobs))

    # Fetch result rows for the final sub-job in the script.
    rows = list(rows_iterable)
    print("{} of the most recent data points.".format(len(rows)))
 


