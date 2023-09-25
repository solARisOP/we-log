from django.shortcuts import render, HttpResponse
from blog.models import Post
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

# Create your views here.
def blog_home(request):
    allPosts = Post.objects.all()
    context = {'allPosts' : allPosts}
    return render(request, "blog/blogHome.html", context)

def blog_post(request, slug):
    try:
        post = Post.objects.get(slug = slug)
        context = {'post' : post}
        return render(request, "blog/blogPost.html", context)
    except ObjectDoesNotExist:
        messages.error(request, "No such blog exists")
        allPosts = Post.objects.all()
        context = {'allPosts' : allPosts}
        return render(request, "blog/blogHome.html", context)
