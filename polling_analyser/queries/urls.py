from django.urls import path
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal
from . import views

urlpatterns = [
    path('', views.QueryList.as_view(), name='home'),
    path('create/', views.QueryCreate.as_view(), name='create'),
    path('query/<int:pk>/', views.QueryDetail.as_view(), name='detail'),
]
