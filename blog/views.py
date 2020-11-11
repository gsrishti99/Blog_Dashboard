from django.shortcuts import render, HttpResponse, redirect
from .models import Post
from django.contrib import messages

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/home.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.view += 1
    post.save()

    