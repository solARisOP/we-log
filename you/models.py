from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification')

    NEW = 0
    CURRENT = 1
    READ = 2
    notify_choices = (
        (NEW, 'new'),
        (CURRENT, 'current'),
        (READ, 'read'),
    )
    status = models.IntegerField(choices=notify_choices, default=NEW)

    link = models.TextField(null=False, default="/")
    timeStamp = models.DateTimeField(default=now)
    description = models.TextField(max_length=155)
