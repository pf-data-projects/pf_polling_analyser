from django.contrib import admin
from .models import Query


@admin.register(Query)
class SessionAdmin(admin.ModelAdmin):
    """
    A class to register session data on admin site.
    """
    list_display = ('user', 'survey_name', 'starting_qid', 'ending_qid', 'created_at')
    list_filter = ('user', 'survey_name')
    search_fields = ('user__username', 'survey_name')
    