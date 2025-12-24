from django.urls import path
from .views import BlogHomeView, ProfileView, MyProfileView, EditProfileView, follow_toggle, AboutView, PrivacyPolicyView, ContactView

app_name = 'blog'

urlpatterns = [
    path('', BlogHomeView.as_view(), name='home'),
    path('my-profile/', MyProfileView.as_view(), name='my_profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('follow/<str:username>/', follow_toggle, name='toggle_follow'),
    path('about/', AboutView.as_view(), name='about'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('contact/', ContactView.as_view(), name='contact'),
]