from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Author
from .forms import AuthorForm

def test(request):
    data = Author.objects.all()
    return render(request, 'test.html', {'data': data})

def home(request):
    data = Author.objects.exclude(user=request.user)
    return render(request, 'home.html', {'data': data})

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

