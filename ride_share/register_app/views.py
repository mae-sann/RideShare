from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm", "")
        if not email or not password or not confirm:
            error = "All fields are required."
        elif password != confirm:
            error = "Passwords do not match."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif User.objects.filter(username=email).exists():
            error = "Email already registered."
        else:
            User.objects.create_user(username=email, email=email, password=password)
            return redirect('')
    return render(request, "register_app/register.html", {"error": error})
