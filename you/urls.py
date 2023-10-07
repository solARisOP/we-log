from django.urls import path
from you import views 

urlpatterns = [
    path('', views.profilePage, name = "profilePage"),
    path('profileEdit', views.profileEdit, name = "profileEdit"),
    path('otpverif', views.otpVerificater, name = "otpVerificater"),
    path('passreset', views.passwordReseter, name = "passwordReseter"),
    path('signup', views.handleSignup, name = "handleSignup"),
    path('login', views.handleLogin, name = "handleLogin"),
    path('logout', views.handleLogout, name = "handleLogout"),
    path('check', views.checker, name = "checker"),
    path('follow/<str:username>', views.follow, name = "follow"),
    path('unfollow/<str:username>', views.unFollow, name = "unFollow"),
]