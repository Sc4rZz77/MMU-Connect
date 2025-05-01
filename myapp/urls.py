from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("test", views.test, name="test"),
    path("", views.home, name="home"),
    path("about-us/", views.aboutus, name="about-us"),
    path("chat/", views.chat, name="chat"),
    path("contact/", views.contact, name="contact"),
    path("feature/", views.feature, name="feature"),
    path('edit_profile/', views.edit_profile , name='edit_profile'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

