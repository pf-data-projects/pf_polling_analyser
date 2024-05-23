"""
Maps the urls for the views associated with the bot_checker app.
"""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
from django.urls import path
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal
from . import views

urlpatterns = [
    path('bot_check/', views.upload_bots, name="bot_check"),
    path('fetch_checks/', views.fetch_checks, name="fetch_checks"),
    path('task_status/', views.task_status, name='task_status')
]
