"""
Maps the urls for the views associated with the bot_checker app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('bot_check/', views.upload_bots, name="bot_check"),
]
