from django.urls import path, include
from blog import views 

urlpatterns = [
    path('', views.blog_home, name = "blog-home"),
    path('<str:slug>', views.blog_post, name = "blog-post"),
]