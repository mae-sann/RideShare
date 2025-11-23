from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from .models import RideShareUser
from accounts_app.views import send_verification_email 
from profile_app.supabase_utils import get_supabase_client, update_or_create_profile  

def register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Create Django user
        user = User.objects.create_user(
            username=form.cleaned_data['email'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            is_active=False
        )
        
        # Create RideShareUser (local Django)
        RideShareUser.objects.create(
            user=user,
            phone=form.cleaned_data['phone'],
            student_id=form.cleaned_data['student_id']
        )

        # ✅ ADD THIS: Create profile in Supabase
        user_id_str = str(user.id)
        profile_data = {
            'user_id': user_id_str,
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'username': form.cleaned_data['email'],  # Using email as username
            'email': form.cleaned_data['email'],
            'phone_number': form.cleaned_data['phone'],  # Save phone to Supabase
            'full_name': f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}".strip(),
        }
        
        try:
            success = update_or_create_profile(user_id_str, profile_data)
            if not success:
                print("Warning: Failed to create Supabase profile for user", user_id_str)
        except Exception as e:
            print("Error creating Supabase profile:", str(e))
            # Don't fail registration if Supabase fails, just log it

        send_verification_email(user)

        return render(request, "register_app/verify_notice.html", {
            "email": user.email
        })
    return render(request, "register_app/register.html", {"form": form})