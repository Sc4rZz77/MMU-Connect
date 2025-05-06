from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("test", views.test, name="test"),
    path("", views.home, name="home"),
    path("about-us/", views.aboutus, name="about-us"),
    path("chat/", views.chat, name="chat"),
    path("contact/", views.contact, name="contact"),
    path("feature/", views.feature, name="feature"),
    path('edit_profile/', views.edit_profile , name='edit_profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

