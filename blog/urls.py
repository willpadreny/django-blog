from django.urls import path
from .views import BlogHomeView, follow_toggle

app_name = 'blog'

urlpatterns = [
    path('', BlogHomeView.as_view(), name='home'),
    path('follow/<str:username>/', follow_toggle, name='toggle_follow'),
]