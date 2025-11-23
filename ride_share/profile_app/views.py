import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .supabase_utils import get_supabase_client, upload_profile_picture_to_supabase, update_or_create_profile
import logging

logger = logging.getLogger(__name__)

@login_required
def upload_profile_picture(request):
    """Handle profile picture upload separately"""
    print("=== DEBUG: upload_profile_picture function called ===")
    
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        try:
            file = request.FILES['profile_picture']
            user_id_str = str(request.user.id)
            
            print(f"DEBUG: Uploading profile picture for user {user_id_str}")
            print(f"DEBUG: File: {file.name}, Size: {file.size}, Type: {file.content_type}")
            
            # Upload to Supabase Storage (using the renamed function)
            file_url = upload_profile_picture_to_supabase(file, user_id_str)
            print(f"DEBUG: Upload successful, URL: {file_url}")
            
            # Update profile in Supabase using the helper function
            profile_data = {
                'profile_picture_url': file_url,
                'updated_at': 'now()'
            }
            
            print(f"DEBUG: Updating database with profile data: {profile_data}")
            success = update_or_create_profile(user_id_str, profile_data)
            
            if success:
                print("DEBUG: Database update successful")
                messages.success(request, 'Profile picture updated successfully!')
            else:
                print("DEBUG: Database update failed")
                messages.error(request, 'Error updating profile picture in database.')
                
            return redirect('profile')
            
        except Exception as e:
            print(f"DEBUG: Upload error: {str(e)}")
            import traceback
            print(f"DEBUG: Full traceback: {traceback.format_exc()}")
            messages.error(request, f'Error uploading profile picture: {str(e)}')
    
    print("DEBUG: No file found in request or not POST method")
    return redirect('profile')

@login_required
def profile_view(request):
    """View for user profile management."""
    
    print(f"=== DEBUG: Profile view called ===")
    print(f"User: {request.user}, ID: {request.user.id}")
    print(f"Request method: {request.method}")
    
    # Handle profile picture upload via separate form
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        print("DEBUG: Profile picture upload detected in profile_view")
        return upload_profile_picture(request)
    
    # Initialize Supabase client
    try:
        supabase = get_supabase_client()
        print("DEBUG: Supabase client connected successfully")
    except ValueError as e:
        print(f"DEBUG: Supabase connection error: {e}")
        messages.error(request, 'Server configuration error. Please contact administrator.')
        return render(request, 'profile_app/profile_new.html')
    
    # Handle profile information update
    if request.method == 'POST' and 'update_profile' in request.POST:
        print("DEBUG: Profile info update detected")
        try:
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            username = request.POST.get('username', '')
            phone_number = request.POST.get('phone', '')
            
            print(f"DEBUG: Form data - First: {first_name}, Last: {last_name}, Username: {username}, Phone: {phone_number}")
            
            # Convert user ID to string for Supabase
            user_id_str = str(request.user.id)
            
            # Update Django user
            user = request.user
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if username:
                user.username = username
            user.save()
            print("DEBUG: Django user updated")
            
            # ✅ ADDED: Update local RideShareUser phone number if it exists
            try:
                if hasattr(request.user, 'rideshareuser'):
                    request.user.rideshareuser.phone = phone_number
                    request.user.rideshareuser.save()
                    print("DEBUG: RideShareUser phone number updated")
            except Exception as e:
                print(f"DEBUG: Warning - Could not update RideShareUser phone: {str(e)}")
            
            # Update profile in Supabase using the helper function
            profile_data = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'phone_number': phone_number,
                'full_name': f"{first_name} {last_name}".strip(),
                'updated_at': 'now()'
            }
            
            success = update_or_create_profile(user_id_str, profile_data)
            
            if success:
                messages.success(request, 'Profile updated successfully!')
            else:
                messages.error(request, 'Error updating profile in database.')
                
            return redirect('profile')
            
        except Exception as e:
            print(f"DEBUG: Profile update error: {str(e)}")
            messages.error(request, f'Error updating profile: {str(e)}')
    
    # GET request - fetch current data
    try:
        user = request.user
        user_id_str = str(user.id)
        
        print("DEBUG: Fetching profile data from Supabase...")
        response = supabase.table('profiles').select('*').eq('user_id', user_id_str).execute()
        print(f"DEBUG: Profile fetch response: {response}")
        
        profile_data = response.data[0] if response.data else {}
        print(f"DEBUG: Profile data from Supabase: {profile_data}")
        
        # ✅ ADDED: If phone number is missing in Supabase, get it from local RideShareUser
        if not profile_data.get('phone_number'):
            try:
                if hasattr(request.user, 'rideshareuser'):
                    local_phone = request.user.rideshareuser.phone
                    if local_phone:
                        profile_data['phone_number'] = local_phone
                        print(f"DEBUG: Using local phone number: {local_phone}")
                        
                        # ✅ OPTIONAL: Auto-update Supabase with the local phone number
                        update_data = {'phone_number': local_phone, 'updated_at': 'now()'}
                        update_or_create_profile(user_id_str, update_data)
                        print("DEBUG: Auto-updated Supabase with local phone number")
            except Exception as e:
                print(f"DEBUG: Warning - Could not fetch local phone: {str(e)}")
        
        # Check if profile picture URL exists and is accessible
        if profile_data.get('profile_picture_url'):
            print(f"DEBUG: Profile picture URL found: {profile_data['profile_picture_url']}")
        else:
            print("DEBUG: No profile picture URL found")
        
        context = {
            'user': user,
            'profile_data': profile_data,
        }
        
    except Exception as e:
        print(f"DEBUG: Profile fetch error: {str(e)}")
        messages.error(request, f'Error loading profile: {str(e)}')
        context = {
            'user': request.user,
            'profile_data': {},
        }
    
    return render(request, 'profile_app/profile_new.html', context)