from django.urls import path
from . import views

urlpatterns = [
    path('find_rides/', views.find_rides, name='find_rides'),
    path('post_ride/', views.post_ride, name='post_ride'),
]