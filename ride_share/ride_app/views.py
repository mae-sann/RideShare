from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostRideForm, BookRideForm
from .models import Ride, Booking

# Create your views here.

@login_required
def post_ride(request):
    """Render the post ride page"""
    if request.method == 'POST':
        form = PostRideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.driver = request.user
            ride.status = 'open'
            ride.save()
            return redirect('find_rides')
    else:
        form = PostRideForm()

    return render(request, "dashboard_app/post_ride.html", {'form': form})


@login_required
def find_rides(request):
    """Render the find rides page"""
    rides = Ride.objects.filter(status='open').order_by('start_date', 'start_time')

    # Optional filter
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    date = request.GET.get('date')

    #For ride matching
    if origin:
        rides = rides.filter(origin__icontains=origin)
    if destination:
        rides = rides.filter(destination__icontains=destination)
    if date:
        rides = rides.filter(start_date=date)
    return render(request, "dashboard_app/find_rides.html", {'rides':rides})


@login_required
def book_ride(request, ride_id):
    """Handle ride booking"""
    ride = get_object_or_404(Ride, id=ride_id)
    
    # Prevent driver from booking their own ride
    if ride.driver == request.user:
        messages.error(request, "You cannot book your own ride.")
        return redirect('find_rides')
    
    # Check if user has an active posted ride
    user_active_ride = Ride.objects.filter(driver=request.user, status='open').first()
    if user_active_ride:
        messages.error(request, "You cannot book a ride while you have an active posted ride. Please close or complete your ride first.")
        return redirect('find_rides')
    
    # Check if user already booked this ride
    existing_booking = Booking.objects.filter(ride=ride, passenger=request.user).first()
    if existing_booking:
        messages.warning(request, "You have already booked this ride.")
        return redirect('find_rides')
    
    if request.method == 'POST':
        form = BookRideForm(request.POST)
        if form.is_valid():
            num_seats = form.cleaned_data['num_seats']
            
            # Check available seats
            if num_seats > ride.seats_available:
                messages.error(request, f"Only {ride.seats_available} seats available.")
                return redirect('find_rides')
            
            # Create booking
            booking = form.save(commit=False)
            booking.ride = ride
            booking.passenger = request.user
            booking.status = 'confirmed'
            booking.save()
            
            # Update available seats
            ride.seats_available -= num_seats
            if ride.seats_available == 0:
                ride.status = 'full'
            ride.save()
            
            messages.success(request, "Ride booked successfully!")
            return redirect('my_bookings')
    else:
        form = BookRideForm()
    
    return render(request, "dashboard_app/book_ride.html", {'form': form, 'ride': ride})


@login_required
def my_bookings(request):
    """Show user's bookings"""
    bookings = Booking.objects.filter(passenger=request.user).order_by('-created_at')
    return render(request, "dashboard_app/my_bookings.html", {'bookings': bookings})

@login_required
def my_rides(request):
    """Show user's posted rides"""
    rides = Ride.objects.filter(driver=request.user).order_by('-start_date', '-start_time')
    return render(request, "dashboard_app/my_rides.html", {'rides': rides})

@login_required
def close_ride(request, ride_id):
    """Close a posted ride"""
    ride = get_object_or_404(Ride, id=ride_id)
    
    # Check if user is the ride owner
    if ride.driver != request.user:
        messages.error(request, "You can only close your own rides.")
        return redirect('find_rides')
    
    # Close the ride
    ride.status = 'closed'
    ride.save()
    
    messages.success(request, "Ride closed successfully!")
    return redirect('my_rides')