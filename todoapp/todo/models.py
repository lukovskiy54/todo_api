from django.db import models
from django.conf import settings

class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    user_email = models.CharField(max_length=100)

    def __str__(self):
        return self.title
