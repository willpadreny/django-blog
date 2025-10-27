from django.views.generic import FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .forms import SignupForm
from .forms import SigninForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

class SignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        user = User.objects.create_user(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
            email = form.cleaned_data['email']
        )
        login(self.request, user)
        return super().form_valid(form)

class SigninView(FormView):
    template_name = 'accounts/signin.html'
    form_class = SigninForm
    success_url = reverse_lazy('blog:home') # change to home url

    def form_valid(self, form):
         
         username = form.cleaned_data['username']
         password = form.cleaned_data['password']

         user = authenticate(self.request, username=username, password=password)

         if user is not None:
            login(self.request, user)
            return super().form_valid(form)
         else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('/')
