from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('upload-picture/', views.upload_profile_picture, name='upload_profile_picture'),
]