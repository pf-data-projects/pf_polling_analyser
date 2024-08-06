"""
Class to register to admin
"""

from django.contrib import admin
from .models import Crossbreak


@admin.register(Crossbreak)
class CrossbreakAdmin(admin.ModelAdmin):
    """
    A class to register the crossbreak instances
    in the admin panel.
    """
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
