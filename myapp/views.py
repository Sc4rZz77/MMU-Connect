from django.shortcuts import render, HttpResponse
from .models import Author


# Create your views here.
def test (request):
    data = Author.objects.all()  # Fetch all authors
    return render(request, 'test.html', {'data': data})

def home (request):
    data = Author.objects.all()  # Fetch all authors
    return render(request, 'home.html', {'data': data})
    
def aboutus(request):
    return render(request, "about-us.html")

def chat(request):
    return render(request, "chat.html")

def contact(request):
    return render(request, "contact.html")

def feature(request):
    return render(request, "feature.html")
