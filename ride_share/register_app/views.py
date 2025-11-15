import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from register_app.models import EmailVerificationToken

def send_verification_email(user):
    # Create or get a token
    token_obj, created = EmailVerificationToken.objects.get_or_create(user=user)
    verification_link = f"https://rideshare-nxo3.onrender.com/accounts/verify/{token_obj.token}/"

    # Email content
    subject = "Verify your email"
    html_content = f"""
<p>Hi {user.first_name} {user.last_name},</p>
<p>Please verify your email by clicking this link:</p>
<p><a href="{verification_link}">{verification_link}</a></p>
<p>Thank you!</p>
    """

    # Must match your verified sender in SendGrid
    from_email = "auditormechole@gmail.com"
    to_email = user.email

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"✅ Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")