"""
### DEPRECATED UNTIL FURTHER NOTICE ###

The idea behind this app is that the user could
query the alchemer API directly and save the details
of that search for future use.

There is a potential future plan to create our own database of polling
results data. The idea is that we could query our own database quickly
rather than being limited by alchemer's 240rpm limit.

While originally designed to get data for polling tables
straight from Alchemer (this didn't work quickly or efficiently enough),
this app could be adapted in future to query our own database

"""

from django.db import models
from django.contrib.auth.models import User


class Query(models.Model):
    """
    A class to handle session data.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey_name = models.CharField(max_length=200)
    starting_qid = models.IntegerField()
    ending_qid = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Displays records in order of when they
        were created in db.
        """
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}'s Session for {self.survey_name}"
