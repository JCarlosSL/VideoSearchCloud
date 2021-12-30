from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"

table_id = 'invertible-env-332913.videosearch.labelVideos'
#table_id = 'invertible-env-332913.videosearch.etiquetaVideos'

"""schema = [
    bigquery.SchemaField("etiqueta", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("nombre", "STRING", mode="REQUIRED"),
]
table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)"""

#table = client.get_table(table_id) 


# View table properties
#print(
#    "Got table '{}.{}.{}'.".format(table.project, table.dataset_id, table.table_id)
#)
#print("Table schema: {}".format(table.schema))
#print("Table description: {}".format(table.description))
#print("Table has {} rows".format(table.num_rows))