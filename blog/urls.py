from django.urls import path
from .views import BlogHomeView

app_name = 'blog'

urlpatterns = [
    path('', BlogHomeView.as_view(), name='home'),
]