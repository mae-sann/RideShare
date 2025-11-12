from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Profile
import re

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 09123456789'
            }),
        }
        labels = {
            'phone': 'Phone Number',
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError('Phone number should contain only digits.')
        if phone and len(phone) < 10:
            raise forms.ValidationError('Phone number should be at least 10 digits long.')
        return phone

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture_url']
        widgets = {
            'profile_picture_url': forms.FileInput(attrs={
                'class': 'hidden',
                'id': 'id_profile_picture',
                'accept': 'image/jpeg,image/png'
            })
        }
        labels = {
            'profile_picture_url': 'Profile Picture'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture_url'].required = False

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text and validation
        self.fields['new_password1'].help_text = None
        self.fields['new_password1'].validators = []
        self.fields['new_password2'].validators = []
        
        # Update widget attributes
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': self.fields[field].label
            })