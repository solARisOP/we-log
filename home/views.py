from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact, UserProfile
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
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

def handleSignup(request):
    if request.method == 'POST':
        currentPath = request.session['currpath']
        username= request.POST['username']
        fname= request.session['fname']
        lname= request.session['lname']
        email= request.session['email']
        pass1= request.POST['pass1']
        pass2= request.POST['pass2']
        desc = request.session['desc']
        # avatar = request.session['avatar']
        if not username.isalnum():
            messages.error(request, "username must contain only aphabets and numbers")
            return redirect(currentPath)
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect(currentPath)

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        myuserprofile = UserProfile.objects.create(description = desc, user = request.user)
        myuserprofile.save()
        messages.success(request, "Your weLog account has been created successfully")
        return redirect(currentPath)

    else:
        return HttpResponse("Request not found", status=400)
    
def handleLogin(request):
    if request.method == 'POST':
        currentPath = request.META.get('HTTP_REFERER').split("127.0.0.1:8000")[1]
        loginusername= request.POST['loginusername']
        loginpassword= request.POST['loginpassword']
        user = authenticate(username = loginusername, password = loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged In")
            return redirect(currentPath)
        
        else:
            messages.error(request, "Invalid Credentials please try again")
            return redirect(currentPath)

    else:
        return HttpResponse('Invalid request', status=404)

def handleLogout(request):
    if request.user.is_authenticated:
        currentPath = request.META.get('HTTP_REFERER').split("127.0.0.1:8000")[1]
        logout(request)
        messages.success(request, "Successfully logged Out")
        return redirect(currentPath)
    else:
        return HttpResponse('Invalid request', status=404)