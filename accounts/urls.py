from django.urls import path
from django.views.generic import TemplateView
from .views import *


app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('done/', TemplateView.as_view(template_name='accounts/done.html'), name='done'),
    path('logout/', logout_view, name='logout'),
]