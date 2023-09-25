from django.shortcuts import render, HttpResponse
from home.models import Contact
from django.contrib import messages
from blog.models import Post

def home(request):
    return render(request, "home/home.html")

def about(request):
    return render(request, "home/about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill in the form correctly")
        else:
            contact = Contact(name = name, email = email, phone = phone, content = content)
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
        allPostsAuthor = Post.objects.filter(author__icontains = query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)
    
    if len(allPosts) == 0:
        messages.warning(request, "No search results found please refine your query")
    params = {'allPosts' : allPosts, 'query' : query}
    return render(request, "home/search.html", params)
    # return HttpResponse("this is search")