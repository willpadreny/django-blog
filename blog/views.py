from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post

class BlogHomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    login_url = '/accounts/signin/' 