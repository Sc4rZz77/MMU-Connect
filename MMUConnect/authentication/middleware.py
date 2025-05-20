from django.shortcuts import redirect
from django.contrib.auth import logout

class TwoFactorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Skip if not authenticated or not MMU student
        if not (request.user.is_authenticated and 
               request.user.email.endswith('@student.mmu.edu.my')):
            return response
            
        # Force logout if 2FA not verified
        if not request.session.get('2fa_verified'):
            logout(request)
            return redirect('verify_2fa?next=' + request.path)
            
        return response