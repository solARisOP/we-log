from django.urls import path
from blog import views 

urlpatterns = [
    path('updater', views.updateBlog, name = "updateBlog"),
    path('update/<int:sno>', views.updateView, name = "updateView"),
    path('delete/<int:sno>', views.deleteBlog, name = "deleteBlog"),
    path('postblog', views.postBlog, name = "postBlog"),
    path('createblog', views.createBlog, name = "createBlog"),
    path('postComment', views.postComment, name = "postComment"),
    path('', views.blogHome, name = "blogHome"),
    path('<int:slug>', views.blogPost, name = "blogPost"),
]