from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from .views import ai_chat, ForceOTPLoginView
from .two_factor_views import verify_2fa

urlpatterns = [
    path('', views.signup, name='signup'),  # home route as signup
    path('login/', ForceOTPLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('verify-2fa/', verify_2fa, name='verify_2fa'),
    path('home/', views.home, name='home'),
    path('about-us/', views.aboutus, name='about-us'),
    path('chat/', views.chat, name='chat'),
    path('contact/', views.contact, name='contact'),
    path('feature/', views.feature, name='feature'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('api/chat/', ai_chat, name='ai_chat'),
    path('send-email/', views.send_email, name='send_email'),
    path('test', views.test, name='test'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


