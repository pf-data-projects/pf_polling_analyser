"""
This file defines the url paths that django will
look for when running views from this app's views.py
file.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_data'),
    path('weight/', views.weight_data, name='weight_data'),
    path('download/', views.download_csv, name='download_csv'),
    path('weights_download/', views.download_weights, name='download_weights'),
    path('instructions/', views.GuideView.as_view(), name='instructions'),
]
