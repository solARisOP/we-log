from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment, ViewCount, Like, Dislike
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from blog.templatetags import extras
from django.urls import reverse
from you.models import Notification
from django.http import JsonResponse
import json
from django.db.models import Count
from django.core.paginator import Paginator

def blogHome(request):
    request.session.pop("query", None)
    allPosts = Post.objects.all().order_by('-timeStamp')
    pages = 10
    paginate = Paginator(allPosts, pages, orphans=len(allPosts)%pages)
    page = 1
    if 'page' in request.GET:
        page = request.GET['page']
    page_obj = paginate.get_page(page)
    context = {'allPosts' : page_obj}
    return render(request, "blog/blogHome.html", context)

def blogPost(request, slug):
    try:
        post = Post.objects.get(slug = slug)
        like = 0
        dislike = 0
        if request.user.is_authenticated:
            ViewCount.objects.get_or_create(post = post, user = request.user)
            
            if Like.objects.filter(post = post, user = request.user).exists():
                like = 1
            elif Dislike.objects.filter(post = post, user = request.user).exists():
                dislike = 1

        comments = BlogComment.objects.filter(post = post, parent = None)
        replies = BlogComment.objects.filter(post = post).exclude(parent = None)

        replyDict = {}
        for reply in replies:
            parent = reply.parent.sno
            if parent not in replyDict:
                replyDict[parent] = []
            replyDict[parent].append(reply)

        context = {'post' : post, 'comments' : comments, 'replyDict' : replyDict, 'like' : like, 'dislike' : dislike}
        return render(request, "blog/blogPost.html", context)
    except ObjectDoesNotExist:
        messages.error(request, "No such blog exists")
        allPosts = Post.objects.all()
        context = {'allPosts' : allPosts}
        return render(request, "blog/blogHome.html", context)

def postComment(request):
    if request.method=="POST":
        comment = request.POST["comment"]
        user = request.user
        slug = request.POST["postSlug"]
        parentSno = request.POST["parentSno"]
        post =  Post.objects.get(slug = slug)
        if parentSno == "":
            comment = BlogComment(comment = comment, user = user, post = post)
            messages.success(request, "comment posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment = comment, user = user, post = post, parent = parent)
            messages.success(request, "reply posted successfully")
        comment.save()

        if request.user != post.user:
            notify = Notification.objects.create(user = post.user, link = reverse('blogPost', kwargs={'slug' : post.slug})+"#"+comment.slug, description = f'''{request.user.username} has commented on your Blog "{post.title}" - "{comment.comment}"''')

    return redirect(f"/blog/{post.slug}") 

def createBlog(request):
    if request.user.is_authenticated:
        return render(request, "blog/blogCreate.html")
    else:
        return redirect('/you')

def postBlog(request):
    if (request.user.is_authenticated) and (request.method=="POST"):
        title = request.POST["title"]
        content = request.POST["blog"]
        description = request.POST["desc"]

        if request.FILES.get('avatar'):
            avatar = request.FILES['avatar']
            post = Post.objects.create(title = title, content = content, description = description, user = request.user, avatar = avatar)

        else:
            post = Post.objects.create(title = title, content = content, description = description, user = request.user)
        
        followers = request.user.followers.all()

        notifications_to_create = [
            Notification(user = follower.user,
                         link = reverse('blogPost', kwargs={'slug':post.slug}),
                         description = f'''{post.user.username} has posted a new blog "{post.title}"'''
                        )
            for follower in followers
        ]

        Notification.objects.bulk_create(notifications_to_create)

        post.save()
        messages.success(request, "You blog has been successfully posted")
        return redirect('/you')
    
def updateView(request, slug):
    if request.user.is_authenticated:
        currentPath = request.META.get('HTTP_REFERER').split("vercel.app")[1]
        post = Post.objects.get(slug = slug)
        if post is not None and post.user == request.user:
            context = {'post' : post}
            return render(request, "blog/blogUpdate.html", context)
        else:
            messages.error(request, "cannot understand you request")
            return redirect(currentPath)
    
    return HttpResponse("very bad request", status= 405)

def updateBlog(request, slug):
    if request.user.is_authenticated:
        title = request.POST['utitle']
        content = request.POST['ublog']
        description = request.POST['udesc']

        post = Post.objects.get(slug = slug)
        if post is not None and post.user == request.user:
            post.title = title
            post.content = content
            post.description = description
            if request.FILES.get('uavatar'):
                post.avatar = request.FILES['uavatar']
            post.save()
            messages.success(request, "Your Post has been successfully updated")
            return redirect("/you")
        else:
            messages.error(request, "cannot understand you request")
            return redirect("/") 
        
    return HttpResponse("very bad request", status= 405)        

def deleteBlog(request, slug):
    if request.user.is_authenticated:
        currentPath = request.META.get('HTTP_REFERER').split("vercel.app")[1]
        post = Post.objects.get(slug = slug)

        if post is not None and post.user == request.user:
            post.delete()
            messages.success(request, "Your Post has been successfully deleted")
            Notification.objects.filter(link = reverse('blogPost', kwargs={'slug':post.slug})).delete()
            return redirect(currentPath)
        
        else:
            messages.error(request, "cannot understand you request")
            return redirect(currentPath) 
        
        
    return HttpResponse("very bad request", status= 405)

def LikesDislikes(request, slug):
    if request.user.is_authenticated and request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        opt = data['message']
        post = Post.objects.get(slug = slug) 

        if opt == 1:
            Like.objects.create(user = request.user, post = post)
            Dislike.objects.filter(user = request.user, post = post).delete()
            response = {'message' : 1}

        elif opt == 2:
            Like.objects.filter(user = request.user, post = post).delete()
            response = {'message' : 2}

        elif opt == 3:
            Dislike.objects.create(user = request.user, post = post)
            Like.objects.filter(user = request.user, post = post).delete()
            response = {'message' : 3}

        elif opt == 4:
            Dislike.objects.filter(user = request.user, post = post).delete()
            response = {'message' : 4}

        return JsonResponse(response)

    return HttpResponse("sorry cantunderstand your request", status=404)  

def sortBy(request, opt):
    if 'query' in request.session:
        title = request.session['query']
        allPostsTitle = Post.objects.filter(title__icontains = title)
        allPostsTitle = allPostsTitle.annotate(view_count=Count('viewcount'), love=Count('likes'))
        allPostsContent = Post.objects.filter(content__icontains = title)
        allPostsContent = allPostsContent.annotate(view_count=Count('viewcount'), love=Count('likes'))
        allPostsDescription = Post.objects.filter(description__icontains = title)
        allPostsDescription = allPostsDescription.annotate(view_count=Count('viewcount'), love=Count('likes'))
        allPosts = allPostsTitle.union(allPostsContent, allPostsDescription)
    else:
        allPosts = Post.objects.all()
        allPosts = allPosts.annotate(view_count=Count('viewcount'), love=Count('likes'))

    if opt == 1:
        allPosts = allPosts.order_by('-view_count')
    elif opt == 2:
        allPosts = allPosts.order_by('-love')
    elif opt == 3:
        allPosts = allPosts.order_by('-timeStamp')

    pages = 10
    paginate = Paginator(allPosts, pages, orphans=len(allPosts)%pages)
    page = 1
    if 'page' in request.GET:
            page = request.GET['page']
    page_obj = paginate.get_page(page)
    context = {'allPosts' : page_obj}

    return render(request, "blog/blogHome.html", context)

