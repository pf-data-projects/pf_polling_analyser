from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_data'),
    path('weight/', views.weight_data, name='weight_data'),
]
