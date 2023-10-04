from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('contact', views.contact, name = "contact"),
    path('search', views.search, name = "search"),
    path('account', views.accounts, name = "accounts"),
    path('account/<str:slug>', views.authorProfile, name = "authorProfile"),
]