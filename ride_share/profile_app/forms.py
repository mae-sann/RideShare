from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=150, required=True)
    phone = forms.CharField(max_length=20, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set up form fields with classes
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

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