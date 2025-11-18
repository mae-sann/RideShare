from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_ride, name='post_ride'),
    path('find/', views.find_rides, name='find_rides'),
    path('book/<int:ride_id>/', views.book_ride, name='book_ride'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]