from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from .views import ai_chat


urlpatterns = [
    path("test", views.test, name="test"),
    path("home/", views.home, name="home"),
    path("about-us/", views.aboutus, name="about-us"),
    path("chat/", views.chat, name="chat"),
    path("contact/", views.contact, name="contact"),
    path("feature/", views.feature, name="feature"),
    path('edit_profile/', views.edit_profile , name='edit_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('api/chat/', ai_chat, name='ai_chat'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
