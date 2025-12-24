from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
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

        # Check 2FA status
        from django_otp.plugins.otp_totp.models import TOTPDevice
        has_2fa = TOTPDevice.objects.filter(user=self.request.user, confirmed=True).exists()
        context['has_2fa'] = has_2fa

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

class ProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'posts'
    login_url = '/accounts/signin/'

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=self.profile_user).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.profile_user

        # Check if current user is following the profile user
        is_following = Follow.objects.filter(
            follower=self.request.user,
            following=self.profile_user
        ).exists()
        context['is_following'] = is_following

        return context

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'profile-input',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'profile-input',
                'placeholder': 'Email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'profile-input',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'profile-input',
                'placeholder': 'Last Name'
            })
        }

class MyProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/my_profile.html'
    context_object_name = 'posts'
    login_url = '/accounts/signin/'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get followers - users who follow me
        followers = Follow.objects.filter(following=self.request.user).select_related('follower')
        context['followers'] = followers
        context['followers_count'] = followers.count()

        # Get following - users I follow
        following = Follow.objects.filter(follower=self.request.user).select_related('following')
        context['following'] = following
        context['following_count'] = following.count()

        # Check 2FA status
        from django_otp.plugins.otp_totp.models import TOTPDevice
        has_2fa = TOTPDevice.objects.filter(user=self.request.user, confirmed=True).exists()
        context['has_2fa'] = has_2fa

        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'blog/edit_profile.html'
    login_url = '/accounts/signin/'
    success_url = reverse_lazy('blog:my_profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'blog/privacy_policy.html'

