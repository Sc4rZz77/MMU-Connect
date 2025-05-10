import os
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Author
from .forms import AuthorForm
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.http import JsonResponse
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed
import re
from huggingface_hub import InferenceClient
from dotenv import load_dotenv




def test(request):
    data = Author.objects.all()
    return render(request, 'test.html', {'data': data})

@login_required
def home(request):
    data = Author.objects.exclude(user=request.user)
    return render(request, "home.html", {"data": data})

def aboutus(request):
    return render(request, "about-us.html")

def chat(request):
    return render(request, "chat.html")

def contact(request):
    return render(request, "contact.html")

def feature(request):
    return render(request, "feature.html")

@login_required
def edit_profile(request):
    author, created = Author.objects.get_or_create(user=request.user)  # Ensure user has a profile
    
    if request.method == "POST":
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return redirect("home")  # Redirect after saving
    else:
        form = AuthorForm(instance=author)

    return render(request, "edit_profile.html", {"form": form})  # Allow users to edit their profile

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Secure password handling
            user.save()
            login(request, user)  # Log in the user immediately after signup
            return redirect("home")  # Redirect to homepage
    else:
        form = SignupForm()
    
    return render(request, "signup.html", {"form": form})
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
    api_key=os.getenv("HF_TOKEN"),  # Replace with your actual API key
)

def ai_chat(request):
    user_input = request.GET.get("message", "").strip()

    if not user_input:
        return JsonResponse({"error": "No message provided"}, status=400)

    # Normalize user input for rule-based matching
    normalized_input = re.sub(r'[^\w\s]', '', user_input.lower())

    # Rule-based responses
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
        r"\byour favorite color\b": "I’d say electric blue—it’s the color of data, connection, and creativity!"
    }

    # Check if user input matches a rule-based response
    for pattern, response in response_map.items():
        if re.search(pattern, normalized_input):
            return JsonResponse({"reply": response})

    # If no rule matches, fallback to Qwen AI for a creative response
    try:
        ai_response = client.chat.completions.create(
            model="qwen/qwen3-235b-a22b:free",
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
    

        # Just return the full response without limiting words
        return JsonResponse({"reply": generated_text})

    except Exception as e:
        return JsonResponse({"reply": f"Oops, something went wrong. Error: {str(e)}"})




