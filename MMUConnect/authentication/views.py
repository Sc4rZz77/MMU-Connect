from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

class ForceOTPLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if user.email.endswith('@student.mmu.edu.my'):
            self.request.session['2fa_user_id'] = user.id
            return redirect('verify_2fa')
        return super().form_valid(form)