# accounts/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset_password/', views.reset_password, name='reset_password'),
]
