"""
Maps the urls for the views associated with the bot_checker app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('bot_check/', views.upload_bots, name="bot_check"),
    path('fetch_checks/', views.fetch_checks, name="fetch_checks"),
]
