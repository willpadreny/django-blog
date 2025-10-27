from django import forms
from django.contrib.auth.models import User
import re
from captcha.fields import CaptchaField

class SignupForm(forms.Form):

    username = forms.CharField(
        widget = forms.TextInput(attrs={'placeholder': 'Username'}), 
        max_length = 100,
        error_messages={'max_length': 'Username cannot exceed 100 characters.'}
    )
    
    email = forms.EmailField(
        widget = forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    
    password = forms.CharField(
        widget = forms.PasswordInput(attrs={'placeholder': 'Password'}),
        max_length = 150,
        error_messages={'max_length': 'Password cannot exceed 150 characters.'}
    )

    confirm_password = forms.CharField(
        widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        max_length = 150,
        error_messages={'max_length': 'Password cannot exceed 150 characters.'}
    )
    
    captcha = CaptchaField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 12:
            raise forms.ValidationError("Password length must be greater than 12 characters")
        
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter")
        
        if len(re.findall(r'\d', password)) < 2:
            raise forms.ValidationError("Password must contain at least two numbers")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError('Password must contain at least one special character.')
        
        return password

        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class SigninForm(forms.Form):
    username = username = forms.CharField(
        widget = forms.TextInput(attrs={'placeholder': 'Username'}), 
        max_length = 100,
        error_messages={'max_length': 'Username cannot exceed 100 characters.'}
    )
    
    password = forms.CharField(
        widget = forms.PasswordInput(attrs={'placeholder': 'Password'}),
        max_length = 150,
        error_messages={'max_length': 'Password cannot exceed 150 characters.'}
    )

    