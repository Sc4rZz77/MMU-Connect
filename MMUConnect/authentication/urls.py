from django.urls import path
from .views import CustomLoginView
from .two_factor_views import verify_2fa

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('verify-2fa/', verify_2fa, name='verify_2fa'),
    
]