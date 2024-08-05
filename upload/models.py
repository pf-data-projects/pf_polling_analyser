"""
A model to handle data needed for crossbreaks.
The Crossbreak class has the django dunder method
for easy identification.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
from django.db import models
from django.contrib.auth.models import User

class Crossbreak(models.Model):
    """
    A class to handle save-able custom
    crossbreaks that users can create, edit,
    read, and delete from the database and
    include in forms when running the table maker. 
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    question = models.CharField(max_length=1000)
    Answers = models.CharField(max_length=1000)

    class Meta:
        """
        Ensures that crossbreak records are ordered by
        creation date in the database, and are named
        in an intuitive way.
        """
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}'s crossbreak: {self.name}"
