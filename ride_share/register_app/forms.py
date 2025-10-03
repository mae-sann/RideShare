from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.Form):
    first_name = forms.CharField(label="First name", max_length=30, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your first name',
        'required': True
    }))
    last_name = forms.CharField(label="Last name", max_length=30, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your last name',
        'required': True
    }))
    email = forms.EmailField(label="Student Email", max_length=254, widget=forms.EmailInput(attrs={
        'placeholder': 'your.email@university.edu',
        'required': True
    }))
    phone = forms.CharField(label="Phone Number", max_length=15, widget=forms.TextInput(attrs={
        'placeholder': '+1234567890',
        'required': True
    }))
    student_id = forms.CharField(label="Student ID", max_length=20, widget=forms.TextInput(attrs={
        'placeholder': '12-3456-789',
        'required': True
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Create a strong password',
        'required': True,
        'minlength': 6
    }))
    confirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm your Password',
        'required': True,
        'minlength': 6
    }))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")
        if password and confirm and password != confirm:
            self.add_error('confirm', "Passwords do not match.")
        if password and len(password) < 6:
            self.add_error('password', "Password must be at least 6 characters.")