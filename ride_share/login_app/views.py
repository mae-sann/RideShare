from django.shortcuts import render

def index(request):
      error = None
      if request.method == "POST":
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "")
            if not email or not password:
                  error = "Both fields are required."
            elif len(password) < 6:
                  error = "Password must be at least 6 characters."
      # Add more validation as needed
      else:
            # Authenticate user here
            pass
      return render(request, "login_app/login.html", {"error": error})