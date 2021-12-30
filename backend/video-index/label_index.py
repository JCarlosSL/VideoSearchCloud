import os
import json
from os import path
from google.cloud import storage, vision
import subprocess

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

def detect_labels(source_blob_name):
  client = vision.ImageAnnotatorClient.from_service_account_json('credentials.json')
  file_name = os.path.abspath(source_blob_name)
  labelss=set()
  with io.open(file_name, 'rb') as image_file:
    content = image_file.read()
    image = vision.Image(content=content)
    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    for label in labels:
      print(label.description)
      labelss.add(label.description)
  return labelss


def label_thumbs(event, context):
  bucket = event['bucket']
  filename = event['name']
  
  basename = os.path.splitext(filename)[0]
  out_movie = '/tmp/'+filename
  out_json = basename+'.json'
  
  download_blob(bucket,filename,out_movie)
  data = {}
  data['id'] = basename
  
  list_labels = list(detect_labels(out_movie))
  data['labels'] = list_labels
  
  try:
    with open('/tmp/'+out_json, 'w') as fp:
      json.dump(data,fp)
    upload_blob('video-indexs','/tmp/'+out_json,basename)
  except Exception as e:
    return False
  return True
