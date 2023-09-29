from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return "Message from " + (self.name if self.name else self.user.username)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    avatar = models.ImageField(null=True)

    def __str__(self):
        return self.user.username + f"({self.user.first_name} {self.user.last_name})"