"""
This models file contains all classes pertaining
to bug report data storage in the db.
"""

from django.db import models
from django.contrib.auth.models import User


class ReportMessage(models.Model):
    """
    A class for handling bug report data
    in the database.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="report_message"
    )
    date_sent = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_sent']
    
    def __str__(self):
        return(f"{self.user}'s issue report")
