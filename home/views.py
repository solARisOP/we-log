from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact, UserProfile
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    return render(request, "home/home.html")

def accounts(request):
    users = User.objects.all()
    context = {'users' : users}
    return render(request, 'home/authors.html', context)

def authorProfile(request, slug):
    user_ = User.objects.get(username = slug)
    if request.user.is_authenticated and request.user == user_:
        return redirect('/you')
    allPosts = Post.objects.filter(user = user_)
    try:
        profile = UserProfile.objects.get(user = user_)
        context = {'profile' : profile, 'allPosts' : allPosts, 'user_' : user_}
    except ObjectDoesNotExist:
        context = {'allPosts' : allPosts, 'user_' : user_}
    return render(request, 'account/user_profile.html', context)

def contact(request):
    if request.method == "POST":
        content = request.POST['content']
        if request.user.is_authenticated:
            contact = Contact(user = request.user, content = content)
            contact.save()
            messages.success(request, "Your message has been sent")
            return render(request, "home/contact.html")
            
        name = request.POST['name']
        email = request.POST['email']
        contact = Contact(name = name, email = email, content = content)
        contact.save()
        messages.success(request, "Your message has been sent")
    return render(request, "home/contact.html")

def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains = query)
        allPostsContent = Post.objects.filter(content__icontains = query)
        allPosts = allPostsTitle.union(allPostsContent)
    
    if len(allPosts) == 0:
        messages.warning(request, "No search results found please refine your query")
    params = {'allPosts' : allPosts, 'query' : query}
    return render(request, "home/search.html", params)