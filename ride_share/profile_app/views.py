import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.conf import settings
from .forms import ProfileForm, ProfilePictureForm, CustomPasswordChangeForm
from .models import Profile
from .supabase_utils import upload_profile_picture, delete_profile_picture

@login_required
def profile_view(request):
    """View for user profile management."""
    # Get or create user profile
    profile = get_object_or_404(Profile, user=request.user)
    
    # Initialize forms with current instance data
    profile_form = ProfileForm(instance=profile)
    password_form = CustomPasswordChangeForm(request.user)
    picture_form = ProfilePictureForm(instance=profile)
    
    if request.method == 'POST':
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            picture_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
            if picture_form.is_valid():
                # Handle file upload to Supabase
                file = request.FILES['profile_picture']
                try:
                    # Upload new profile picture
                    file_url = upload_profile_picture(file, request.user.id)
                    if file_url:
                        # Delete old profile picture if exists
                        if profile.profile_picture_url:
                            delete_profile_picture(profile.profile_picture_url)
                        
                        # Update profile with new picture URL
                        profile.profile_picture_url = file_url
                        profile.save()
                        messages.success(request, 'Profile picture updated successfully!')
                    else:
                        messages.error(request, 'Failed to upload profile picture. Please try again.')
                except Exception as e:
                    messages.error(request, f'Error uploading profile picture: {str(e)}')
                return redirect('profile')
        
        # Update profile information
        elif 'update_profile' in request.POST:
            # Update user fields
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.username = request.POST.get('username', '')
            
            # Update profile fields
            profile_form = ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                try:
                    # Save user first
                    user.save()
                    
                    # Then save profile
                    profile = profile_form.save(commit=False)
                    # Update full_name based on first and last name
                    profile.full_name = f"{user.first_name} {user.last_name}".strip()
                    profile.save()
                    
                    messages.success(request, 'Profile updated successfully!')
                    return redirect('profile')
                except Exception as e:
                    messages.error(request, f'Error updating profile: {str(e)}')
            else:
                # If form is invalid, show error messages
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                
                # Add username validation error if any
                if 'username' in request.POST:
                    username = request.POST['username']
                    if not username:
                        messages.error(request, 'Username is required')
                    elif len(username) < 3:
                        messages.error(request, 'Username must be at least 3 characters long')
                    elif User.objects.exclude(pk=user.pk).filter(username=username).exists():
                        messages.error(request, 'This username is already taken')
                        
        # Handle password change
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")
        
        # Handle password change
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        
        # Handle profile picture upload
        elif 'upload_picture' in request.FILES:
            picture_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
            if picture_form.is_valid():
                try:
                    file = request.FILES['profile_picture_url']
                    
                    # Delete old profile picture if exists
                    if profile.profile_picture_url:
                        delete_profile_picture(profile.profile_picture_url)
                    
                    # Upload new profile picture
                    url = upload_profile_picture(file, str(request.user.id))
                    
                    # Save the URL to the profile
                    profile.profile_picture_url = url
                    profile.save()
                    
                    messages.success(request, 'Profile picture updated successfully!')
                    return redirect('profile')
                    
                except Exception as e:
                    messages.error(request, f'Error uploading profile picture: {str(e)}')
    
    # Prepare context for the template
    profile_form = ProfileForm(instance=profile)
    profile_picture_form = ProfilePictureForm()
    
    context = {
        'profile_form': profile_form,
        'profile_picture_form': profile_picture_form,
        'user': request.user,
    }
    
    return render(request, 'profile_app/profile_new.html', context)


class ChangePasswordView(PasswordChangeView):
    """View for changing user password."""
    form_class = CustomPasswordChangeForm
    template_name = 'profile_app/change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)
