from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Author
from .forms import AuthorForm
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout


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



