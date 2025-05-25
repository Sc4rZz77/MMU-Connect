import os
from django.contrib.auth.decorators import login_required
from .models import Author
from .forms import AuthorForm
from .forms import SignupForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.http import JsonResponse
import re
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import time
from django.contrib import messages
from myapp.forms import SignupForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.core.cache import cache
from .otp_utils import send_otp_email
from django.contrib.auth import get_user_model
import random


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

    return render(request, "edit_profile.html", {
        "form": form,
        "MEDIA_URL": settings.MEDIA_URL  # 👈 This enables {{ MEDIA_URL }} in the template
    })

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

class CustomLoginView(auth_views.LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:  
            return redirect("home")  # Redirect to homepage if logged in
        response = super().dispatch(request, *args, **kwargs)

        # Set session expiry to 7 days (604800 seconds)
        if request.POST.get("remember_me"):  
            request.session.set_expiry(604800)  
        else:
            request.session.set_expiry(0)  # Session ends when the user closes the browser
        
        return response
    
def logout_view(request):
    logout(request)  # Clear user session
    request.session.flush()  # Ensure full session reset
    
    response = redirect("login")  # Redirect user to login page
    response.set_cookie("sessionid", "", expires=0)  # Expire session cookie immediately
    return response

load_dotenv()
client = InferenceClient(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("HF_TOKEN"),  
)

def ai_chat(request):
    user_input = request.GET.get("message", "").strip()

    if not user_input:
        return JsonResponse({"error": "No message provided"}, status=400)
    
    # Insert chat history to be remembered (omitted for simplicity)
    # Allow machine learning (omitted for simplicity)

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
            # Simulate typing animation by sending the full response in chunks
            def typing_animation(response):
                sentence_chunks = [response]  # Single chunk for the full response
                for chunk in sentence_chunks:
                    time.sleep(0.5)  # Simulate typing delay
                    yield chunk  # Yield the whole sentence in one go

            return JsonResponse(
                {"reply": list(typing_animation(response))},
                content_type="application/json"
            )

    try:
        ai_response = client.chat.completions.create(
            model="qwen/qwen3-1.7b:free",
            messages=[
                {"role": "system", "content": "/no_think"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            top_p=0.8,
            extra_body={
                "top_k": 20,    # Vendor-specific extension
                "min_p": 0      # Vendor-specific extension
            }
        )
        generated_text = ai_response['choices'][0]['message']['content'].strip()

        # Simulate typing animation for the full AI response
        def typing_animation(response):
            sentence_chunks = [response]  # Send the whole response at once
            for chunk in sentence_chunks:
                time.sleep(0.5)  # Adjust delay between chunks
                yield chunk  # Yield the full response at once

        return JsonResponse(
            {"reply": list(typing_animation(generated_text))},
            content_type="application/json"
        )

    except Exception as e:
        return JsonResponse({"reply": f"Oops, something went wrong. Error: {str(e)}"})

def send_email(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        full_message = f"From: {name} <{email}>\n\nMessage:\n{message}"

        send_mail(
            subject="New Contact Form Message",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['scarmanthegamer@gmail.com', 'MUHAMMAD.MUHYIDEEN.BARAKA@student.mmu.edu.my', 'NIMALEN.RAMA.KRISHNAN@student.mmu.edu.my'],
            fail_silently=False,
        )
        return render(request, 'home.html') 

    return redirect('contact')  

User = get_user_model()

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
