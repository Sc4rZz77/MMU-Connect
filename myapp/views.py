import os
import re
import time
import random
from dotenv import load_dotenv

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.mail import send_mail
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse

from huggingface_hub import InferenceClient

from .models import Author, Like
from .forms import AuthorForm, SignupForm
from .otp_utils import send_otp_email

User = get_user_model()
client = InferenceClient()

def test(request):
    data = Author.objects.all()
    return render(request, 'test.html', {'data': data})

@login_required
def home(request):
    return render(request, "home.html")

def feature(request):
    data = Author.objects.exclude(user=request.user)
    return render(request, "feature.html", {"data": data})

def aboutus(request):
    return render(request, "about-us.html")

def chat(request):
    return render(request, "chat.html")

def livechat(request):
    return render(request, "livechat.html")

def contact(request):
    return render(request, "contact.html")

@login_required
def edit_profile(request):
    author, created = Author.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
    else:
        form = AuthorForm(instance=author)

    return render(request, "edit_profile.html", {"form": form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        response = super().dispatch(request, *args, **kwargs)

        if request.POST.get("remember_me"):
            request.session.set_expiry(604800)  # 7 days
        else:
            request.session.set_expiry(0)  # Close browser ends session

        return response

def logout_view(request):
    logout(request)
    request.session.flush()
    response = redirect("login")
    response.set_cookie("sessionid", "", expires=0)
    return response

@login_required
def ai_chat(request):
    user_input = request.GET.get("message", "").strip()
    if not user_input:
        return JsonResponse({"error": "No message provided"}, status=400)

    normalized_input = re.sub(r'[^\w\s]', '', user_input.lower())

    response_map = {
        r"\bhello\b|\bhi+\b|\bhey+\b|\bhelo+\b|\bhola\b|\bhii\b|\bhelloo+\b": "Hey there! How can I brighten your day?",
        r"\bhow (are|r) (you|u)\b|\bhow do you feel\b|\bhow’s it going\b": "I'm doing fantastic! What about you?",
        r"\bwhat( is|'s)? this app (about|for)\b|\bwhat does this app do\b|\bwhat app is this\b": "It's a social discovery app helping people meet new friends in a modern, fun way!",
        r"\btell me a joke\b|\bjoke please\b|\banother joke\b|\bmake me laugh\b|\bfunny\b": "Why did the computer get cold? Because it forgot to close its Windows!",
        r"\bbye+\b|\bgoodbye\b|\bsee you\b|\bcya\b": "Goodbye! Remember, I'm just a message away whenever you need me!",
        r"\bwhat('?s| is) your name\b|\bwho are you\b|\bwhat are you\b|\bwho r u\b": "I'm Vin AI, your intelligent assistant built to help and chat with you!",
        r"\bthanks\b|\bthank you\b|\bthx\b|\bty\b": "You're welcome! Always happy to help.",
        r"\bwho (made|built|created) you\b|\bwho are the developers\b": "I was built with care by Shaarvin, Muhyideen, Nimalen, and Sashvin!",
        r"\bcontact (support|developers)\b|\bhow do i contact\b|\bget help\b": "Just head to the About Us page and drop them a message!",
        r"\bwho is your boss\b|\bwho do you obey\b|\byour master\b": "That’s easy! My one and only boss is Shaarvin, the King!",
        r"\banother\b|\bmore\b|\bone more\b": "Sure! But let me know what you're looking for :)",
        r"\bi love you\b": "That's so sweet of you! I love chatting with you too! ❤️",
        r"\bhelp\b|\bi need help\b|\bcan you help me\b": "Absolutely! Just tell me what's troubling you.",
        r"\bi will see you\b|\bsee you later\b": "See you soon! I'll be right here when you return.",
        r"\byour favorite color\b": "I’d say electric blue—it’s the color of data, connection, and creativity!",
    }

    for pattern, response in response_map.items():
        if re.search(pattern, normalized_input):
            return JsonResponse({"reply": [response]}, content_type="application/json")

    try:
        ai_response = client.chat.completions.create(
            model="meta-llama/llama-3.3-8b-instruct:free",
            messages=[
                {"role": "system", "content": "/no_think"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            top_p=0.8,
            extra_body={
                "top_k": 20,
                "min_p": 0
            }
        )
        generated_text = ai_response['choices'][0]['message']['content'].strip()
        return JsonResponse({"reply": [generated_text]}, content_type="application/json")
    except Exception as e:
        return JsonResponse({"reply": f"Oops, something went wrong. Error: {str(e)}"})

def send_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"From: {name} <{email}>\n\nMessage:\n{message}"

        send_mail(
            subject="New Contact Form Message",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[
                'scarmanthegamer@gmail.com',
                'MUHAMMAD.MUHYIDEEN.BARAKA@student.mmu.edu.my',
                'NIMALEN.RAMA.KRISHNAN@student.mmu.edu.my'
            ],
            fail_silently=False,
        )
        return render(request, 'home.html')

    return redirect('contact')

class ForceOTPLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if user.email.endswith('@student.mmu.edu.my'):
            self.request.session['2fa_user_id'] = user.id
            return redirect('verify_2fa')
        return super().form_valid(form)

def verify_2fa(request):
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

    user_id = request.session.get('2fa_user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    send_otp_email(user)
    return render(request, 'two_factor/verify.html')

from django.shortcuts import redirect
from .models import UserProfile  # or whatever model you're using

def like_profile(request, liked_user_id):
    # example logic – update to your needs
    if request.user.is_authenticated:
        liked_user = UserProfile.objects.get(id=liked_user_id)
        request.user.profile.likes.add(liked_user)
        return redirect('homepage')  # change 'homepage' to your redirect target
    return redirect('login')  # or wherever you want to send unauthenticated users
