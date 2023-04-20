from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

posts =[
    {
        'author':'David Masila',
        'title':'Blog post 1',
        'content':'First post content',
        'date_posted':'April 20th 2023'
    },
    {
        'author':'David Mwendwa',
        'title':'Blog post 2',
        'content':'Second post content',
        'date_posted':'April 24th 2023'
    }
]


def home(request):
    context = {
        'posts' : posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return HttpResponse("<h1>Blog About</h1>")