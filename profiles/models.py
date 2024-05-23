"""
A model to handle data needed for user profiles.
The Profile class has the handy django dunder method
for easy identification

This file also includes a function to handle the
automatic generation of profiles when a user instance is
created and added to the database.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    A class to handle user profile data.
    Most importantly, it defines whether or not
    a user has permission to accesss API.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        """
        Ensures that profile records are ordered by
        creation date in the database.
        """
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}'s Profile"


def create_profile(sender, instance, created, **kwargs):
    """
    Auto-generates a profile for a new user.
    """
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)
