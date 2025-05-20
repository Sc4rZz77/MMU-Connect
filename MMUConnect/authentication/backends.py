from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class OTPBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                if user.email.endswith('@student.mmu.edu.my'):
                    request.session['2fa_user_id'] = user.id 
                    return None  
                return user
        except User.DoesNotExist:
            return None