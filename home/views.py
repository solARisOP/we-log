from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact, UserProfile
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

def home(request):
    allPosts = Post.objects.all()[0:10]
    context = {'allPosts' : allPosts}
    return render(request, "home/home.html", context)

def accounts(request, **kwargs):
    if kwargs.keys():
        user = User.objects.get(username = kwargs['username'])
        type_ = kwargs['type']
        profiles = user.followers.all() if type_ == 'followers' else user.following.all()
        f = 1 if type_ == 'followers' else  0
        pages = 9
        paginate = Paginator(profiles, pages, orphans=len(profiles)%pages)
        page = 1
        if 'page' in request.GET:
            page = request.GET['page']
        page_obj = paginate.get_page(page)
        context = {'profiles' : page_obj, 'uzer' : user, 'f' : f}
    else:
        users = User.objects.all()
        pages = 9
        paginate = Paginator(users, pages, orphans=len(users)%pages)
        page = 1
        if 'page' in request.GET:
            page = request.GET['page']
        page_obj = paginate.get_page(page)
        context = {'users' : page_obj}

    return render(request, 'home/authors.html', context)

def accountSearch(request, **kwargs):
    user = User.objects.get(username = kwargs['username'])
    type_ = kwargs['type']
    profiles = user.followers.all() if type_ == 'followers' else user.following.all()
    f = 1 if type_ == 'followers' else  0

    name = request.GET['name']
    q1 = UserProfile.objects.filter(user__username__icontains = name)
    q2 = UserProfile.objects.filter(user__first_name__icontains = name)
    q3 = UserProfile.objects.filter(user__last_name__icontains = name)

    q = q1.union(q2, q3)
    profiles = q.intersection(profiles)

    pages = 9
    paginate = Paginator(profiles, pages, orphans=len(profiles)%pages)
    page = 1
    if 'page' in request.GET:
        page = request.GET['page']
    page_obj = paginate.get_page(page)
    context = {'profiles' : page_obj, 'uzer' : user, 'f' : f}

    return render(request, 'home/authors.html', context)

def authorProfile(request, username):
    user_ = User.objects.get(username = username)
    if request.user.is_authenticated and request.user == user_:
        return redirect('/you')
    
    allPosts = Post.objects.filter(user = user_).order_by('-timeStamp')
    pages = 5
    paginate = Paginator(allPosts, pages, orphans=len(allPosts)%pages)
    page =1
    if 'page' in request.GET:
        page = request.GET['page']
    page_obj = paginate.get_page(page)
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user = request.user)
        followers = user_.followers.all()
        if profile in followers:
            x = '1'
        else:
            x = '0'
        context = {'x' : x, 'allPosts' : page_obj, 'user_' : user_}
    else:
        context = {'allPosts' : page_obj, 'user_' : user_}

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
    if 'query' in request.GET:
        title = request.GET['query']
        allPostsTitle = Post.objects.filter(title__icontains = title)
        allPostsContent = Post.objects.filter(content__icontains = title)
        allPostsDescription = Post.objects.filter(description__icontains = title)
        
        allPosts = allPostsTitle.union(allPostsContent, allPostsDescription)

        pages = 10
        paginate = Paginator(allPosts, pages, orphans=len(allPosts)%pages)
        page = 1
        if 'page' in request.GET:
            page = request.GET['page']
        page_obj = paginate.get_page(page)
        context = {'allPosts' : page_obj}

        request.session["query"] = title
        return render(request, 'blog/blogHome.html', context)

    elif 'name' in request.GET:
        name = request.GET['name']
        q1 = User.objects.filter(username__icontains = name)
        q2 = User.objects.filter(first_name__icontains = name)
        q3 = User.objects.filter(last_name__icontains = name)

        users = q1.union(q2, q3)

        pages = 9
        paginate = Paginator(users, pages, orphans=len(users)%pages)
        page = 1
        if 'page' in request.GET:
            page = request.GET['page']
        page_obj = paginate.get_page(page)
        context = {'users' : page_obj}

        return render(request, 'home/authors.html', context)
    
    else:
        return HttpResponse("sorry cannot understant your request", status=404)