from django import forms
from .models import Author
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'self_bio', 'profile_picture', 'faculty', 'gender']

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@student.mmu.edu.my'):
            raise forms.ValidationError("Email must be an MMU student email (@student.mmu.edu.my).")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Use a different email.")

        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable help texts
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = ''
