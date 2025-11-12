from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
