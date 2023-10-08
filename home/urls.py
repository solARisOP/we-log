from django.urls import path, include, re_path
from home import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('contact', views.contact, name = "contact"),
    path('blog/search', views.search, name = "searchBlog"),
    path('account/search', views.search, name = "searchAuthor"),
    path('account', views.accounts, name = "accounts"),
    re_path(r'^account/(?P<username>\w+)/(?P<type>\w+)/$', views.accounts, name = "accounts"),
    re_path(r'^account/(?P<username>\w+)/(?P<type>\w+)/search$', views.accountSearch, name = "accountSearch"),
    path('account/<str:username>', views.authorProfile, name = "authorProfile"),
]