from django.urls import path
from . import views

urlpatterns = [
    path('table_maker/', views.table_maker_form, name='table_maker'),
    path('table_download/', views.download_tables, name='table_download'),
]
