"""
Maps the urls for the views associated with the excel_tables app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('table_maker/<int:arg1>/', views.table_maker_form, name='table_maker'),
    path('table_download/', views.download_tables, name='table_download'),
    path('scan_table/', views.scan_table, name='scan_table'),
]
