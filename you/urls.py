from django.urls import path
from you import views 

urlpatterns = [
    path('', views.profilePage, name = "profilePage"),
    path('profileEdit', views.profileEdit, name = "profileEdit"),
]