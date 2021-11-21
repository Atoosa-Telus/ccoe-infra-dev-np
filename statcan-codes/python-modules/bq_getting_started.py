from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"

from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

def list_biqquery():
    datasets = list(client.list_datasets())  # Make an API request.
    project = client.project

    if datasets:
        print("Datasets in project {}:".format(project))
        for dataset in datasets:
            print("\t{}".format(dataset.dataset_id))
    else:
        print("{} project does not contain any datasets.".format(project))

def show_dataset_path(dataset_id):
    dataset = client.get_dataset(dataset_id)  # Make a API request.

    full_dataset_id = "{}.{}".format(dataset.project, dataset.path)
    friendly_name = dataset.friendly_name   
    print(
        "Got dataset '{}' with friendly_name '{}'.".format(
            full_dataset_id, friendly_name
        )
    )
def show_dataset_properties(dataset_id):
    dataset = client.get_dataset(dataset_id)  # Make a API request.
    
    print("Description: {}".format(dataset.description))
    print("Labels:")
    labels = dataset.labels
    if labels:
        for label, value in labels.items():
            print("\t{}: {}".format(label, value))
    else:
        print("\tDataset has no labels defined.")

def show_dataset_tables(dataset_id):
    dataset = client.get_dataset(dataset_id)  # Make a API request.
     
    # View tables in dataset.
    print("Tables:")
    tables = list(client.list_tables(dataset))  # Make an API request(s).
    if tables:
        for table in tables:
            print("\t{}".format(table.table_id))
    else:
        print("\tThis dataset does not contain any tables.")

def create_table(table_id):
    schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    ]
    
    #check if table exists, then delete it 
    try:
        table = client.get_table(table_id) 
        client.delete_table(table_id, not_found_ok=True)  # Make an API request.
        print("Deleted table '{}'.".format(table_id))
    except:
        pass

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )

def load_tbl_auto_schema(table_id, source_file):
    #check if table exists, then delete it 
    try:
        table = client.get_table(table_id) 
    #    client.delete_table(table_id, not_found_ok=True)  # Make an API request.
    #    print("Deleted table '{}'.".format(table_id))
    except:
        pass
    
    job_config = bigquery.LoadJobConfig(
        autodetect=True, source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    )
   
    load_job = client.load_table_from_file(
        source_file, table_id, job_config=job_config
    )  # Make an API request.
    load_job.result()  # Waits for the job to complete.
    destination_table = client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))    



if __name__ == "__main__":
    list_biqquery()
    #show_dataset_path("Restful_Statcan")
    #show_dataset_properties("Restful_Statcan")
    show_dataset_tables("Restful_Statcan")

    #dataset = client.get_dataset("Restful_Statcan")  # Make a API request.
    #table_id = dataset.project + '.' + dataset.dataset_id + '.' + 'sample-gcp-table'
    #create_table(table_id)

    dataset = client.get_dataset("Restful_Statcan")  # Make a API request.
    table_id = dataset.project + '.' + dataset.dataset_id + '.' + 'series-info'
    #uri = "gs://cloud-samples-data/bigquery/us-states/us-states.json"
    uri = "https://storage.cloud.google.com/telus-pace-restful-statcanada/statcan_series_info.json"
    source_file = 'statcan_series_info.json'
    load_tbl_auto_schema(table_id, source_file)

 
    show_table_properties(table_id)




    
   