"""
Wires up the report logic to site's urls.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.CreateReportMessage.as_view(), name="report")
]
