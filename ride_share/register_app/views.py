from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from .models import RideShareUser

def register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Create the User
        user = User.objects.create_user(
            username=form.cleaned_data['email'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name']
        )
        # Create the RideShareUser profile
        RideShareUser.objects.create(
            user=user,
            phone=form.cleaned_data['phone'],
            student_id=form.cleaned_data['student_id']
        )
        return redirect('login')
    return render(request, "register_app/register.html", {"form": form})
