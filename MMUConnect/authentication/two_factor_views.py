from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.cache import cache
from .otp_utils import send_otp_email
from django.contrib.auth import get_user_model

User = get_user_model()

def verify_2fa(request):
    # Handle OTP submission
    if request.method == 'POST':
        user_id = request.session.get('2fa_user_id')
        if not user_id:
            return redirect('login')
            
        user = User.objects.get(id=user_id)
        if cache.get(f'otp_{user.id}') == request.POST.get('otp'):
            request.session['2fa_verified'] = True
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        messages.error(request, "Invalid OTP")
    
    # Send new OTP if GET request
    user_id = request.session.get('2fa_user_id')
    if not user_id:
        return redirect('login')
        
    user = User.objects.get(id=user_id)
    send_otp_email(user)
    return render(request, 'two_factor/verify.html')