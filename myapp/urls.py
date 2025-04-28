from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about-us/", views.aboutus, name="about-us"),
    path("chat/", views.chat, name="chat"),
    path("contact/", views.contact, name="contact"),
    path("feature/", views.feature, name="feature"),
]