from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from register_app.models import EmailVerificationToken
from django.contrib.auth.models import User
from django.http import HttpResponse

def send_verification_email(user):
    token_obj, created = EmailVerificationToken.objects.get_or_create(user=user)
    verification_link = f"http://127.0.0.1:8080/accounts/verify/{token_obj.token}/"

    subject = "Verify your email"
    message = f"Hi {user.first_name} {user.last_name},\n\nPlease verify your email by clicking this link:\n{verification_link}\n\nThank you!"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)



def verify_email(request, token):
    try:
        token_obj = EmailVerificationToken.objects.get(token=token)
    except EmailVerificationToken.DoesNotExist:
        return HttpResponse("❌ Invalid or broken verification link.")

    if token_obj.is_valid():
        user = token_obj.user
        user.is_active = True
        user.save()
        token_obj.delete()
        return  redirect('login')
    else:
        return HttpResponse("⚠️ Link expired. Please register again.")

