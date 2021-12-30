from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

table_id = 'invertible-env-332913.videosearch.labelVideos'

data = "Netbook"
query = """
    SELECT etiqueta, nombre FROM `invertible-env-332913.videosearch.labelVideos` WHERE etiqueta='{0}'""".format(data)

query_job = client.query(query)

for row in query_job:
    #print(row)
    print("name={} , etiqueta={}".format(row[1],row[0]))


# View table properties