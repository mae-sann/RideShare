from django import forms

class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={"placeholder": "Enter your email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}))