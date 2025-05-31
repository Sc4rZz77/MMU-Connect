import os
from django.contrib.auth.decorators import login_required
from .models import Author, Message, Like, Dislike
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
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q, BooleanField, ExpressionWrapper
import logging

User = get_user_model()
client = InferenceClient()

def test(request):
    data = Author.objects.all()
    return render(request, 'test.html', {'data': data})

@login_required
@never_cache
def home(request):
    return render(request, "home.html")

@login_required
@never_cache
def feature(request):
    liked_users = Like.objects.filter(liker=request.user).values_list('liked', flat=True)
    disliked_users = Dislike.objects.filter(disliker=request.user).values_list('disliked', flat=True)
    if hasattr(request.user, 'author'):
        my_faculty = getattr(request.user.author, 'faculty', None)
    else:
        my_faculty = None  # Or handle as needed, e.g., redirect or set a default
    authors = Author.objects.exclude(user__in=list(liked_users) + list(disliked_users) + [request.user.id])
    if my_faculty:
        authors = authors.annotate(
            is_same_faculty=ExpressionWrapper(
                Q(faculty=my_faculty),
                output_field=BooleanField()
            )
        ).order_by('-is_same_faculty', 'id')
    data = authors
    return render(request, "feature.html", {"data": data})

@login_required
@never_cache
def aboutus(request):
    return render(request, "about-us.html")

@login_required
@never_cache
def chat(request):
    return render(request, 'chat.html')

@login_required
@never_cache
def livechat(request):
    # Get matched users (excluding yourself)
    matches = Like.objects.filter(liker=request.user).filter(
        liked__likes_given__liked=request.user
    ).values_list('liked', flat=True)
    users = User.objects.filter(id__in=matches).exclude(id=request.user.id)
    authors = Author.objects.filter(user__in=users)

    user_profiles = []
    for user in users:
        author = authors.filter(user=user).first()
        user_profiles.append({
            'username': user.username,
            'full_name': author.name if author and hasattr(author, 'name') else user.get_full_name(),
            'profile_picture': author.profile_picture.url if author and author.profile_picture else '/media/default.jpg',
            # add other fields as needed
        })

    chat_partner = None
    chat_history = []
    chat_partner_username = request.GET.get('user')
    if chat_partner_username:
        try:
            chat_partner = User.objects.get(username=chat_partner_username)
            if is_match(request.user, chat_partner):
                if chat_partner not in users:
                    users.append(chat_partner)
                users_sorted = sorted([request.user.username, chat_partner.username])
                room_group_name = f"chat_{users_sorted[0]}_{users_sorted[1]}"
                chat_history = Message.objects.filter(room=room_group_name).order_by('timestamp')[:50]
            else:
                chat_partner = None
        except User.DoesNotExist:
            chat_partner = None

    # Always include the chat partner for profile pic lookup (if not already in users)
    if chat_partner and chat_partner not in users:
        users.append(chat_partner)

    authors = Author.objects.filter(user__in=users)
    user_profiles = []
    for user in users:
        author = authors.filter(user=user).first()
        user_profiles.append({
            'username': user.username,
            'full_name': author.name if author and hasattr(author, 'name') else user.get_full_name(),
            'profile_picture': author.profile_picture.url if author and author.profile_picture else '/media/author_images/default.jpg'
        })
    
    current_author = Author.objects.filter(user=request.user).first()
    if current_author:
        user_profiles.append({
            'username': request.user.username,
            'full_name': current_author.name if current_author and hasattr(current_author, 'name') else request.user.get_full_name(),
            'profile_picture': current_author.profile_picture.url if current_author and current_author.profile_picture else '/media/author_images/default.jpg'
        })
    
    sidebar_user_profiles = [profile for profile in user_profiles if profile['username'] != request.user.username]

    return render(request, "livechat.html", {
        "user_profiles": user_profiles,
        "sidebar_user_profiles": sidebar_user_profiles,
        "users": users,
        "chat_history": chat_history,
        "chat_partner": chat_partner
    })

@login_required
@never_cache
def contact(request):
    return render(request, "contact.html")

@login_required
@never_cache
def edit_profile(request):
    if not hasattr(request.user, 'author'):
        author = Author.objects.create(user=request.user)  # Create with default values
    form = AuthorForm(request.POST or None, request.FILES or None, instance=request.user.author)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('edit_profile')
    return render(request, 'edit_profile.html', {'form': form})

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
        ip_address = request.META.get('REMOTE_ADDR')
        logging.info(f'Login attempt from IP: {ip_address}')
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
        r"\bhow (are|r) (you|u)\b|\bhow do you feel\b|\bhow's it going\b": "I'm doing fantastic! What about you?",
        r"\bwhat( is|'s)? this app (about|for)\b|\bwhat does this app do\b|\bwhat app is this\b": "It's a social discovery app helping people meet new friends in a modern, fun way!",
        r"\btell me a joke\b|\bjoke please\b|\banother joke\b|\bmake me laugh\b|\bfunny\b": "Why did the computer get cold? Because it forgot to close its Windows!",
        r"\bbye+\b|\bgoodbye\b|\bsee you\b|\bcya\b": "Goodbye! Remember, I'm just a message away whenever you need me!",
        r"\bwhat('?s| is) your name\b|\bwho are you\b|\bwhat are you\b|\bwho r u\b": "I'm Vin AI, your intelligent assistant built to help and chat with you!",
        r"\bthanks\b|\bthank you\b|\bthx\b|\bty\b": "You're welcome! Always happy to help.",
        r"\bwho (made|built|created) you\b|\bwho are the developers\b": "I was built with care by Shaarvin, Muhyideen, Nimalen, and Sashvin!",
        r"\bcontact (support|developers)\b|\bhow do i contact\b|\bget help\b": "Just head to the About Us page and drop them a message!",
        r"\bwho is your boss\b|\bwho do you obey\b|\byour master\b": "That's easy! My one and only boss is Shaarvin, the King!",
        r"\banother\b|\bmore\b|\bone more\b": "Sure! But let me know what you're looking for :)",
        r"\bi love you\b": "That's so sweet of you! I love chatting with you too! ❤️",
        r"\bhelp\b|\bi need help\b|\bcan you help me\b": "Absolutely! Just tell me what's troubling you.",
        r"\bi will see you\b|\bsee you later\b": "See you soon! I'll be right here when you return.",
        r"\byour favorite color\b": "I'd say electric blue—it's the color of data, connection, and creativity!",
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
            model="meta-llama/llama-3.3-8b-instruct:free",
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

@login_required
@never_cache
def like_profile(request, liked_user_id):
    # example logic – update to your needs
    if request.user.is_authenticated:
        liked_user = UserProfile.objects.get(id=liked_user_id)
        request.user.profile.likes.add(liked_user)
        return redirect('homepage')  # change 'homepage' to your redirect target
    return redirect('login')  # or wherever you want to send unauthenticated users

def search_users(request):
    query = request.GET.get('q')
    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(email__icontains=query)
    ) if query else []
    return render(request, 'search_results.html', {'users': users})


@login_required
def chat_history(request):
    other_username = request.GET.get('user')
    if not other_username:
        return JsonResponse({'error': 'No user specified'}, status=400)
    users_sorted = sorted([request.user.username, other_username])
    room = f"chat_{users_sorted[0]}_{users_sorted[1]}"
    messages = Message.objects.filter(room=room).order_by('-timestamp')[:50][::-1]
    data = [
        {
            'sender': msg.sender.username,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for msg in messages
    ]
    return JsonResponse({'messages': data})

@login_required
def like_author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
        if not author.user or author.user == request.user:
            return JsonResponse({'error': 'Invalid like.'}, status=400)
        Like.objects.get_or_create(liker=request.user, liked=author.user)
        if Like.objects.filter(liker=author.user, liked=request.user).exists():
            send_mail(
                'It\'s a Match!',
                f'You and {request.user.username} have liked each other!',
                'from@example.com',
                [request.user.email, author.user.email],
                fail_silently=True,
            )
            return JsonResponse({'status': 'matched'})
        return JsonResponse({'status': 'liked'})
    except Author.DoesNotExist:
        return JsonResponse({'error': 'Author not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

@login_required
def dislike_author(request, author_id):
    author = Author.objects.get(id=author_id)
    if not author.user:
        return JsonResponse({'error': 'This profile is not linked to a user.'}, status=400)
    # Remove like if exists
    Like.objects.filter(liker=request.user, liked=author.user).delete()
    # Add dislike if not already disliked
    Dislike.objects.get_or_create(disliker=request.user, disliked=author.user)
    return JsonResponse({'status': 'disliked'})

@login_required
def people_i_liked(request):
    likes = Like.objects.filter(liker=request.user)
    users = [like.liked for like in likes]
    return render(request, 'people_i_liked.html', {'users': users})

@login_required
def people_who_liked_me(request):
    likes = Like.objects.filter(liked=request.user)
    users = [like.liker for like in likes]
    return render(request, 'people_who_liked_me.html', {'users': users})

@login_required
def matches(request):
    # Users who liked you but you haven't liked them back (pending requests)
    incoming_likes = Like.objects.filter(
        liked=request.user
    ).exclude(
        liker__in=Like.objects.filter(liker=request.user).values_list('liked', flat=True)
    )
    incoming_users = [like.liker for like in incoming_likes]

    # Users you matched with (mutual likes)
    matches = Like.objects.filter(liker=request.user).filter(liked__likes_given__liked=request.user)
    matched_users = User.objects.filter(id__in=matches.values_list('liked', flat=True))

    return render(request, 'matches.html', {
        'incoming_users': incoming_users,
        'matched_users': matched_users,
    })

def is_match(user1, user2):
    return (
        Like.objects.filter(liker=user1, liked=user2).exists() and
        Like.objects.filter(liker=user2, liked=user1).exists()
    )

@login_required
@never_cache
def fun(request):
    return render(request, 'fun.html')

#this is for testing the pushing purpose

#test2