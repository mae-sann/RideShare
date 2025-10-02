from django.shortcuts import render, redirect
from .forms import UserLoginForm

def login(request):
      error = None
      form = UserLoginForm(request.POST or None)
      
      if request.method == "POST" and form.is_valid():
       # email = form.cleaned_data['email']
       # password = form.cleaned_data['password']
        #user = authenticate(request, email=email, password=password)  # or use a custom backend if username != email
        #if user:
            #login(request, user)  # logs the user in, session starts
            return redirect('register')  # change to your dashboard/home page
        #else:
           # error = "Invalid email or password."

      return render(request, "login_app/login.html", {"form": form,"error": error})