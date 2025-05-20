import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user):
    otp = generate_otp()
    cache.set(f'otp_{user.id}', otp, timeout=300)  
    
    send_mail(
        'Your MMU Connect Verification Code',
        f'Your OTP code is: {otp}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )