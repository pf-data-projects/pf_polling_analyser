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
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}'s Session for {self.survey_name}"
