from django.urls import path, include
from blog import views 

urlpatterns = [
    path('postblog', views.postBlog, name = "postBlog"),
    path('createblog', views.createBlog, name = "createBlog"),
    path('postComment', views.postComment, name = "postComment"),
    path('', views.blogHome, name = "blogHome"),
    path('<int:slug>', views.blogPost, name = "blogPost"),
]