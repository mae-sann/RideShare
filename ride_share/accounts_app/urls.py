from django.urls import path
from . import views

urlpatterns = [
    path('verify/<uuid:token>/', views.verify_email, name='verify_email'),
]
