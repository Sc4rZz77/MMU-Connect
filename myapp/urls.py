from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from .views import ai_chat, ForceOTPLoginView
from .two_factor_views import verify_2fa

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # Home route as signup
    path('login/', ForceOTPLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('verify-2fa/', verify_2fa, name='verify_2fa'),
    path('', views.home, name='home'),
    path('about-us/', views.aboutus, name='about-us'),
    path('chat/', views.chat, name='chat'),
    path('contact/', views.contact, name='contact'),
    path('feature/', views.feature, name='feature'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('api/chat/', ai_chat, name='ai_chat'),
    path('send-email/', views.send_email, name='send_email'),
    path('test/', views.test, name='test'),
    path('livechat/', views.livechat, name='livechat'),
    path('search/', views.search_users, name='search_users'),
    path('chat/history/', views.chat_history, name='chat_history'),
    path('like/<int:author_id>/', views.like_author, name='like_author'),
    path('dislike/<int:author_id>/', views.dislike_author, name='dislike_author'),
    path('people-i-liked/', views.people_i_liked, name='people_i_liked'),
    path('people-who-liked-me/', views.people_who_liked_me, name='people_who_liked_me'),
    path('matches/', views.matches, name='matches'),
    path('fun/', views.fun, name='fun'),
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
