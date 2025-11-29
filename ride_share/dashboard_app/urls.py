from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('notifications/read-all/', views.mark_all_read, name='mark_all_read'),
    path('notifications/read/<int:notif_id>/', views.read_notification, name='read_notification'),
]
