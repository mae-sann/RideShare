from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostRideForm, BookRideForm
from .models import Ride, Booking
from django.utils import timezone
from profile_app.supabase_utils import get_supabase_client

# Create your views here.

@login_required
def post_ride(request):
    """Render the post ride page"""

    # Prevent posting if user already has a booking
    active_booking = Booking.objects.filter(
        passenger=request.user,
        status__in=['confirmed', 'pending']  # adjust if you have other statuses
    ).first()

    if active_booking:
        messages.error(
            request,
            "You cannot post a ride while you have an active booking. "
            "Please cancel or complete your booking first."
        )
        return redirect('my_bookings')

    if request.method == 'POST':
        form = PostRideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.driver = request.user
            ride.status = 'open'
            ride.save()
            return redirect('my_rides')
    else:
        form = PostRideForm()

    return render(request, "dashboard_app/post_ride.html", {'form': form})


@login_required
def find_rides(request):
    """Render the find rides page"""
    rides = Ride.objects.filter(status='open').order_by('start_date', 'start_time')
    # Initialize Supabase client
    supabase = get_supabase_client()

    # Fetch profile_picture_url for each driver
    driver_ids = [ride.driver.id for ride in rides]
    response = supabase.table('profiles').select('user_id, profile_picture_url').in_('user_id', driver_ids).execute()
    driver_profiles = {p['user_id']: p['profile_picture_url'] for p in response.data} if response.data else {}

    # Attach profile URL to each ride object for template
    for ride in rides:
        ride.driver_pic = driver_profiles.get(str(ride.driver.id))

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
    """Close a posted ride and mark all bookings as closed"""
    ride = get_object_or_404(Ride, id=ride_id)

    # Check if user is the ride owner
    if ride.driver != request.user:
        messages.error(request, "You can only close your own rides.")
        return redirect('find_rides')

    # Close the ride
    ride.status = 'closed'
    ride.save()

    # Mark all bookings as closed
    Booking.objects.filter(ride=ride).update(status='closed')

    messages.success(request, "Ride closed successfully! All bookings have been marked as closed.")
    return redirect('my_rides')

@login_required
def cancel_booking(request, booking_id):
    """Allow a passenger to cancel their booking"""
    booking = get_object_or_404(Booking, id=booking_id, passenger=request.user)
    ride = booking.ride

    # Optional: prevent cancellation if ride already started
    if ride.start_date < timezone.now().date():
        messages.error(request, "You cannot cancel a ride that has already started.")
        return redirect('my_bookings')

    # Update booking status
    booking.status = 'cancelled'
    booking.save()

    # Return seats to the ride
    ride.seats_available += booking.num_seats
    # If ride was full, reopen it
    if ride.status == 'full':
        ride.status = 'open'
    ride.save()

    messages.success(request, "Your booking has been cancelled successfully.")
    return redirect('my_bookings')