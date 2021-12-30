import os
from os import path
from google.cloud import storage
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

def function_thumbs(event, context):
     bucket = event['bucket']
     filename = event['name']

     basename = os.path.splitext(filename)[0]
     out_movie = '/tmp/'+filename
     frame = '/tmp/'+basename+'.png'
     gif = '/tmp/'+basename+'.gif'

     download_blob(bucket,filename,out_movie)

     os.system(f'ffmpeg -i {out_movie} -ss 00:00:01.000 -vframes 1 {frame}')
     os.system(f'ffmpeg -i {out_movie} -ss 1.0 -t 4.0 -f gif {gif}')

     try:
          upload_blob('video-thumbs',frame,basename)
          upload_blob('video-gifs',gif,basename)
     except Exception as e:
          return False
     return True