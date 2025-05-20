from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .otp_utils import send_otp_email

User = get_user_model()

def verify_2fa(request):
    user_id = request.session.get('2fa_user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)

    # Send OTP once per session
    if not cache.get(f'otp_{user.id}'):
        send_otp_email(user)

    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        if cache.get(f'otp_{user.id}') == otp_input:
            request.session['2fa_verified'] = True
            login(request, user)
            cache.delete(f'otp_{user.id}')  # Optional: delete after success
            return redirect(request.GET.get('next', 'home'))
        messages.error(request, "Invalid OTP")

    return render(request, 'two_factor/verify.html')