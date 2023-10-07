from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from blog.templatetags import extras

def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts' : allPosts}
    return render(request, "blog/blogHome.html", context)

def blogPost(request, slug):
    try:
        post = Post.objects.get(slug = slug)
        comments = BlogComment.objects.filter(post = post, parent = None)
        replies = BlogComment.objects.filter(post = post).exclude(parent = None)

        replyDict = {}
        for reply in replies:
            parent = reply.parent.sno
            if parent not in replyDict:
                replyDict[parent] = []
            replyDict[parent].append(reply)
        print(replyDict)
        context = {'post' : post, 'comments' : comments, 'replyDict' : replyDict}
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

        post.save()
        messages.success(request, "You blog has been successfully posted")
        return redirect('/you')
    
def updateView(request, slug):
    if request.user.is_authenticated:
        currentPath = request.META.get('HTTP_REFERER').split("127.0.0.1:8000")[1]
        post = Post.objects.get(slug = slug)
        if post is not None and post.user == request.user:
            context = {'post' : post}
            return render(request, "blog/blogUpdate.html", context)
        else:
            messages.error(request, "cannot understand you request")
            return redirect(currentPath)
    
    return HttpResponse("very bad request", status= 405)

def updateBlog(request):
    if request.user.is_authenticated:
        title = request.POST['utitle']
        content = request.POST['ublog']
        description = request.POST['udesc']
        slug = request.POST['blogId']

        post = Post.objects.get(slug = slug)
        if post is not None and post.user == request.user:
            post.title = title
            post.content = content
            post.description = description
            if request.FILES.get('avatar'):
                post.avatar = request.FILES['avatar']
            post.save()
            messages.success(request, "Your Post has been successfully updated")
            return redirect("/you")
        else:
            messages.error(request, "cannot understand you request")
            return redirect("/") 
        
    return HttpResponse("very bad request", status= 405)        

def deleteBlog(request, slug):
    if request.user.is_authenticated:
        currentPath = request.META.get('HTTP_REFERER').split("127.0.0.1:8000")[1]
        post = Post.objects.get(slug = slug)

        if post is not None and post.user == request.user:
            post.delete()
            messages.success(request, "Your Post has been successfully deleted")
            return redirect(currentPath)
        
        else:
            messages.error(request, "cannot understand you request")
            return redirect(currentPath) 
        
    return HttpResponse("very bad request", status= 405)
        