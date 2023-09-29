from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from home.models import UserProfile
from blog.models import Post
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def profilePage(request):
    if request.user.is_authenticated:
        allPosts = Post.objects.filter(user = request.user)
        try:
            profile = UserProfile.objects.get(user = request.user)
            context = {'profile' : profile, 'allPosts' : allPosts, 'user_' : request.user}
        except ObjectDoesNotExist:
            context = {'allPosts' : allPosts, 'user_' : request.user}
        return render(request, 'account/user_profile.html', context)
    else :
        return render(request, 'account/non_profile.html')

def profileEdit(request):
    if request.user.is_authenticated:
        fname= request.POST['fname']
        lname= request.POST['lname']
        desc = request.POST['desc']
        # avatar = request.POST['avatar']
        user = User.objects.get(username = request.user.username)
        user.first_name = fname
        user.last_name = lname
        user.save()
        profile = UserProfile.objects.get(user = request.user)
        profile.description = desc
        profile.save()
        return redirect('/you') 