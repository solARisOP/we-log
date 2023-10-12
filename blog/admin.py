from django.contrib import admin
from blog.models import Post, BlogComment, ViewCount, Like, Dislike

# Register your models here.

admin.site.register(Post)
admin.site.register(BlogComment)
admin.site.register(ViewCount)
admin.site.register(Like)
admin.site.register(Dislike)
