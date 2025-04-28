from django.shortcuts import render, HttpResponse

# Create your views here.
def home (request):
    return render(request, "home.html")
    
def aboutus(request):
    return render(request, "about-us.html")

def chat(request):
    return render(request, "chat.html")

def contact(request):
    return render(request, "contact.html")

def feature(request):
    return render(request, "feature.html")