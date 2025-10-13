from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('find-rides/', views.find_rides, name='find_rides'),
    path('post-ride/', views.post_ride, name='post_ride'),
    path('logout/', views.logout_view, name='logout'),
]
