from django.urls import path, include
from .views import UploadAPIView, ListVideosAPIView, FilterVideoAPIview

urlpatterns = [
    path('upload',UploadAPIView.as_view(),name='upload video'),
    path('list',ListVideosAPIView.as_view(),name='list videos'),
    path('filter/<slug:query>', FilterVideoAPIview.as_view(),name='filter video'),
]