"""
This class allows admins to access message data from
the admin panel and perform CRUD operations on them.
"""

from django.contrib import admin
from .models import ReportMessage


@admin.register(ReportMessage)
class ReportMessageAdmin(admin.ModelAdmin):
    """
    A class to handle what actions an admin
    can perform on instances of report messages.
    """
    list_display = ('user', 'date_sent')
    list_filter = ('read',)
    search_fields = ('user__username', 'message',)
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        """
        A function to update message instances read attribute to True
        """
        queryset.update(approved=True)

    def mark_as_unread(self, request, queryset):
        """
        A function to update message instances read attribute to False
        """
        queryset.update(approved=False)
