from django.contrib.auth import views as auth_views
from django.urls import re_path
from .views import *

urlpatterns = [
    # Registration
    re_path(r'^register/$', ClientRegistrationView.as_view(), name='register'),
    
    # Authentication
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
]