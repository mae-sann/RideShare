from django import forms
from django.contrib.auth.models import User
import re

class UserRegisterForm(forms.Form):
    first_name = forms.CharField(label="First name", max_length=30, widget=forms.TextInput(attrs={
        'placeholder': 'Enter first name',
        'required': True
    }))
    last_name = forms.CharField(label="Last name", max_length=30, widget=forms.TextInput(attrs={
        'placeholder': 'Enter last name',
        'required': True
    }))
    email = forms.EmailField(label="Student Email", max_length=254, widget=forms.EmailInput(attrs={
        'placeholder': 'email@cit.edu',
        'required': True
    }))
    phone = forms.CharField(label="Phone Number", max_length=13, widget=forms.TextInput(attrs={
        'placeholder': '+63',
        'required': True
    }))
    student_id = forms.CharField(label="Student ID", max_length=11, widget=forms.TextInput(attrs={
        'placeholder': '##-####-###',
        'required': True
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password',
        'required': True
    }))
    confirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'required': True
    }))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith("@cit.edu"):
            raise forms.ValidationError("Email must end with @cit.edu.")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_phone(self):
        phone_number = self.cleaned_data['phone']
        if not phone_number.startswith("+63"):
            raise forms.ValidationError("Phone number must start with +63.")
        if not phone_number[1:].isdigit(): 
            raise forms.ValidationError("Phone number must be digits after +")
        return phone_number

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        pattern = r'^\d{2}-\d{4}-\d{3}$'
        if not re.match(pattern, student_id):
            raise forms.ValidationError("Student ID must follow format.")
        return student_id
        
    def clean_password(self):
        password = self.cleaned_data['password']
        errors = []

        if len(password) < 6:
            errors.append("Password must be atleast 6 characters long.")
        if not any(c.islower() for c in password):
            errors.append("Password must contain lowercase letter.")
        if not any(c.isupper() for c in password):
            errors.append("Password must contain uppercase letter.")
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least 1 digit.")

        if (errors):
            raise forms.ValidationError(errors)

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")
        if password and confirm and password != confirm:
            self.add_error('confirm', "Passwords do not match.")    