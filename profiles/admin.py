"""
This allows the admin to access all profile data
and perform CRUD functionality on them.
"""

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    A class to handle profiles being registered on admin panel.
    """
    list_display = ('user', 'created_at', 'approved')
    list_filter = ('approved',)
    search_fields = ('user__username',)
    actions = ['approve_profiles', 'disapprove_profiles']

    def approve_profiles(self, request, queryset):
        """
        A function to approve profiles.
        """
        queryset.update(approved=True)

    def disapprove_profiles(self, request, queryset):
        """
        A function to disapprove profiles.
        """
        queryset.update(approved=False)
