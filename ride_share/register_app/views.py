from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from .models import RideShareUser
from accounts_app.views import send_verification_email 

def register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['email'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            is_active=False
        )
        RideShareUser.objects.create(
            user=user,
            phone=form.cleaned_data['phone'],
            student_id=form.cleaned_data['student_id']
        )

        send_verification_email(user)

        return render(request, "register_app/verify_notice.html", {
            "email": user.email
        })
    return render(request, "register_app/register.html", {"form": form})
