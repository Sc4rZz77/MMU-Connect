
import random
from django.core.cache import cache
from django.core.mail import send_mail

def send_otp_email(user):
    otp = f"{random.randint(100000, 999999)}"
    cache.set(f'otp_{user.id}', otp, timeout=300)  # Valid for 5 mins
    send_mail(
        subject=f"Welcome Back,{user.username}!",
        message=f"Your OTP is: {otp}",
        from_email="noreply@example.com",
        recipient_list=[user.email]
    )

