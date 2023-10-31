from django.urls import path
from . import views

urlpatterns = [
    path('table-maker/', views.table_maker_form, name='table-maker')
]