from django import forms
from .models import Author
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Post, Reply


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

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'category']  # Add category field here
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': "What's happening?"}),
            'category': forms.Select(),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1, 'maxlength': 280, 'placeholder': 'Reply...'})
        }