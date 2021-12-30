from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import UploadSerializer
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
# Imports the Google Cloud client library
from google.cloud import storage, bigquery

#videosearch
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client.from_service_account_json('videosearch/cred.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    #blob.upload_from_string(source_file_name)

    return (
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    storage_client = storage.Client.from_service_account_json('videosearch/cred.json')
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    print("Blobs:")
    for blob in blobs:
        print(blob.name)

    if delimiter:
        print("Prefixes:")
        for prefix in blobs.prefixes:
            print(prefix)


class UploadAPIView(generics.CreateAPIView):
    serializer_class= UploadSerializer

    def post(self, request, *args, **kwargs):
        data = request.FILES['file']
        fs = FileSystemStorage(location='media/')
        name = data.name.replace(' ','')
        file = fs.save(name,data)
        url = 'media/'+fs.url(file).split('/')[-1]
        data = upload_blob('videosearch', url,'videos/'+name)
        os.remove(url)
        return Response({"upload":data}, status=status.HTTP_200_OK)

class ListVideosAPIView(generics.ListAPIView):
    serializer_class = UploadSerializer

    def get(self, request, *args, **kwargs):
        list_blobs_with_prefix('videosearch','videos')
        return Response({"list":"data"}, status=status.HTTP_200_OK)


class FilterVideoAPIview(APIView):

    def get(self, request, *args, **kwargs):
        # Construct a BigQuery client object.
        client = bigquery.Client.from_service_account_json('videosearch/cred.json')

        lookup = self.kwargs['query']

        query = """
                SELECT etiqueta, nombre FROM `invertible-env-332913.videosearch.labelVideos` WHERE etiqueta='{0}'""".format(lookup)
                
        query_job = client.query(query)
        
        data = []
        for row in query_job:
            data.append({'name': row[1], 
                            'etiqueta':row[0],
                            'url_video': 'storage.googleapis.com/videosearch/'+row[1]+'.mp4',
                            'url_gif': 'storage.cloud.google.com/video-gifs/'+row[1],
                            'url_image':'storage.cloud.google.com/video-thumbs/'+row[1]})
        return Response(data, status=status.HTTP_200_OK)