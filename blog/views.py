from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django import forms
from .models import Post, Follow


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Post title...',
                'class': 'post-input-title'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': "What's on your mind?",
                'class': 'post-input-content',
                'rows': 4
            })
        }

class BlogHomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    login_url = '/accounts/signin/' 

    def get_queryset(self):
        feed_sort = self.request.GET.get('feed', 'all')

        if feed_sort == 'following':
            following_users = Follow.objects.filter(follower = self.request.user).values_list('following', flat = True)

            return Post.objects.filter(author__in = following_users)
        else:
            return Post.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # add empty form to dictionary
        context['form'] = PostForm()

        # add feed sorting to dictionary
        context['feed_sort'] = self.request.GET.get('feed', 'all')

        # add list of users user is following to dicionary
        following_ids = Follow.objects.filter(follower = self.request.user).values_list('following_id', flat = True)
        context['following_ids'] = list(following_ids)

        return context
    
    # save form to DB
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:home')
        
        # render old posts still incase form is invaild
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

def follow_toggle(request, username):
    user_to_follow = get_object_or_404(User, username = username)

    if request.user != user_to_follow:
        follow_relation = Follow.objects.filter(follower = request.user, following = user_to_follow)

        if follow_relation.exists():
            follow_relation.delete()
        else:
            Follow.objects.create(follower = request.user, following = user_to_follow)

    feed_sort = request.GET.get('feed', 'all')
    return redirect(f"/blog/?feed={feed_sort}")



