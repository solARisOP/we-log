from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.text import slugify
import random, string
# Create your models here.

def post_directory_path(instance, filename):
    return f'post_{instance.sno}/{filename}'

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.TextField()
    content = models.TextField()
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=False)
    timeStamp = models.DateTimeField(default=now, blank=True)
    avatar = models.ImageField(upload_to=post_directory_path, null=True, blank=True)
    
    def __str__(self):
        return self.title + " by " + self.user.username    
    
    def _generate_unique_slug(self):
        unique_slug = slugify(f"{self.user.username}-{self.title}")
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(unique_slug, num)
            num += 1
        return unique_slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)
    
class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.comment[0:15] + "..." + " by " + self.user.username
    
    def _generate_unique_slug(self):
        unique_slug = ''.join(random.choices(string.ascii_letters+string.digits, k=7))

        while BlogComment.objects.filter(slug=unique_slug).exists():
            unique_slug = ''.join(random.choices(string.ascii_letters+string.digits, k=7))

        return unique_slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
            
        super().save(*args, **kwargs)

class ViewCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewcount')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='viewcount')

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  related_name='likes')

class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  related_name='dislikes')

