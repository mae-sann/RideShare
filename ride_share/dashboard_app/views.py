from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ride_app.models import Ride

@login_required
def dashboard(request):
    upcoming_rides = Ride.objects.filter(status='open').order_by('start_date', 'start_time')
    rides_count = upcoming_rides.count()
    kpis = {
        "total_rides": 24,
        "this_week": 8,
        "connections_made": 38,
    }

    recent_activity = [
        {"activity": "Ride completed", "place": "University Campus", "time": "2 hours ago"},
        {"activity": "New ride request", "place": "Shopping Center", "time": "5 hours ago"},
        {"activity": "Ride posted", "place": "Airport", "time": "1 day ago"},
    ]

    context = {
        "kpis": kpis,
        "upcoming_rides": upcoming_rides,
        "rides_count": rides_count,
    }
    return render(request, "dashboard_app/dashboard.html", context)


@login_required
def logout_view(request):
    """Handle user logout and redirect to landing page"""
    print(f"Logout view called by user: {request.user}")
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    print("User logged out, redirecting to landing page")
    return redirect('landing')
