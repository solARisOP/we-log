from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
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
        postSno = request.POST["postSno"]
        parentSno = request.POST["parentSno"]
        post =  Post.objects.get(sno = postSno)
        if parentSno == "":
            comment = BlogComment(comment = comment, user = user, post = post)
            messages.success(request, "comment posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment = comment, user = user, post = post, parent = parent)
            messages.success(request, "reply posted successfully")
        comment.save()
    return redirect(f"/blog/{post.slug}") 