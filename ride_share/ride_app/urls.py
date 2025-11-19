from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_ride, name='post_ride'),
    path('find/', views.find_rides, name='find_rides'),
    path('book/<int:ride_id>/', views.book_ride, name='book_ride'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-rides/', views.my_rides, name='my_rides'),
    path('close/<int:ride_id>/', views.close_ride, name='close_ride'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]