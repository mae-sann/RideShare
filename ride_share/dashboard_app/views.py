from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    kpis = {
        "total_rides": 24,
        "this_week": 8,
        "connections_made": 38,
    }

    upcoming_rides = [
        {"location": "University Main Campus", "time": "8:00 AM • Today", "driver": "Sarah Johnson", "status": "confirmed"},
        {"location": "Downtown Mall", "time": "2:00 PM • Tomorrow", "driver": "Mike Chen", "status": "pending"},
    ]

    recent_activity = [
        {"activity": "Ride completed", "place": "University Campus", "time": "2 hours ago"},
        {"activity": "New ride request", "place": "Shopping Center", "time": "5 hours ago"},
        {"activity": "Ride posted", "place": "Airport", "time": "1 day ago"},
    ]

    context = {
        "kpis": kpis,
        "upcoming_rides": upcoming_rides,
        "recent_activity": recent_activity,
    }
    return render(request, "dashboard_app/dashboard.html", context)

def logout_view(request):
    print(f"Logout view called by user: {request.user}")
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    print("User logged out, redirecting to landing page")
    return redirect('landing')
