from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    read = models.BooleanField(default=False)
    # link = models.URLField(null=False)
    description = models.TextField(max_length=155)
