from django.urls import path
from django.shortcuts import reverse

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal
from . import views

urlpatterns = [
    path('', views.QueryList.as_view(), name='home'),
    path('create/', views.QueryCreate.as_view(success_url='/'), name='create'),
    path('query/<int:pk>/', views.QueryDetail.as_view(), name='detail'),
    path('make-request/<int:pk>/', views.make_request, name='make-request'),
]
