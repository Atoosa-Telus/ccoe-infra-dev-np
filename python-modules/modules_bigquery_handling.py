from google.cloud.bigquery.job import query


def load_query_string(query_file_source):
    with open(query_file_source, 'r') as file:
        return file.read()

def list_datasets():
    
    # [START bigquery_list_datasets]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    datasets = list(client.list_datasets())  # Make an API request.
    project = client.project

    if datasets:
        print("Datasets in project {}:".format(project))
        for dataset in datasets:
            print("\t{}".format(dataset.dataset_id))
    else:
        print("{} project does not contain any datasets.".format(project))
    # [END bigquery_list_datasets]

    return datasets


def client_query(query_string):
    
    # [START bigquery_query]
    from google.cloud import bigquery
    
    # Construct a BigQuery client object.
    client = bigquery.Client()
      
    query_job = client.query(query_string)  # Make an API request.

    print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        print("dataset_id={}, count={}, total_rows={}, size_bytes{}".
                    format(row[0], row["total_rows"], row["tables"], row["size_bytes"]))
    # [END bigquery_query]

def dataset_metadata_read():
    query_string = load_query_string('dataset_size_query.sql')

    datasets = list_datasets()
    for dataset in datasets:
        dataset_query_string = query_string.replace("data_set_name", dataset.dataset_id)
        client_query(dataset_query_string)