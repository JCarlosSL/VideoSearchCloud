import os
from os import path
from google.cloud import storage, bigquery
from urllib.parse import unquote_plus
import json
import sys
from decimal import Decimal

def upload_blob(bucket_name, source_file_name, destination_blob_name):
  """Uploads a file to the bucket."""
  storage_client = storage.Client.from_service_account_json('credentials.json')
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)
  blob.upload_from_filename(source_file_name)
  return (
    "File {} uploaded to {}.".format(
      source_file_name, destination_blob_name)
  )
  
def download_blob(bucket_name, source_blob_name, destination_file_name):
  storage_client = storage.Client.from_service_account_json('credentials.json')
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(source_blob_name)
  blob.download_to_filename(destination_file_name)
  print(
    "Downloaded storage object {} from bucket {} to local file {}.".format(
      source_blob_name, bucket_name, destination_file_name)
    )

def function_add_table(event, context):
  bucket = event['bucket']
  filename = event['name']
  basename = os.path.splitext(filename)[0]
  out_movie = '/tmp/'+filename
  
  download_blob(bucket,filename,out_movie)
  add_data_table(out_movie)

def add_data_table(jsonbatch):
  data_file = open(jsonbatch)

  data = json.load(data_file,parse_float=Decimal)

  client = bigquery.Client()

  table_id = 'invertible-env-332913.videosearch.labelVideos'
  #table = client.get_table(table_id)
  data['id']
  data['labels']
  rows_to_insert = []
  for label in data['labels']:
    print(label)
    rows_to_insert.append({u"etiqueta":label, u"nombre": data['id']})
    
  errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
  if errors == []:
    print("New rows have been added.")
  else:
    print("Encountered errors while inserting rows: {}".format(errors))