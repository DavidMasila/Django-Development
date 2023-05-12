from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post

# @login_required
# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)

@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

@method_decorator(login_required, name='dispatch')
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    #enables us to get the user that is clicked on the links
    #either user is got or a 404 error is raised.
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    #having the model Post here will sync with the url's int:pk
    model = Post

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = ['title','content']

    #allows us to tell the form who the user is.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
#lets try using the mixin for making some views require login
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    #testing our permission to edit a post
    def test_func(self):
        post = self.get_object() #gets the post we are trying to update
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog-home')
    #making sure its passes the Test Mixin test.
    def test_func(self):
        post = self.get_object() #gets the post we are trying to update
        if self.request.user == post.author:
            return True
        return False
    
def about(request):
    return render(request, 'blog/about.html')