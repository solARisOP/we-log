from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('contact', views.contact, name = "contact"),
    path('search', views.search, name = "search"),
    path('signup', views.handleSignup, name = "handleSignup"),
    path('login', views.handleLogin, name = "handleLogin"),
    path('logout', views.handleLogout, name = "handleLogout"),
    path('account', views.accounts, name = "accounts"),
    path('account/<str:slug>', views.authorProfile, name = "authorProfile"),
]