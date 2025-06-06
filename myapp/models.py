from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null if needed
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    self_bio = models.TextField(default="No bio available")
    profile_picture = CloudinaryField(
        folder='author_images/',
        default='author_images/default.jpg'
    )

    GENDER_CHOICES = [
        ('Unknown Gender', 'Unknown Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Unknown Gender')

    FACULTY_CHOICES = [
        ('Not specified', 'Default'),
        ('FCI', 'Faculty of Computing'),
        ('FOE', 'Faculty of Engineering'),
        ('FCM', 'Faculty of Creative Multimedia'),
        ('FOM', 'Faculty of Management'),
        ('FAC', 'Faculty of Applied Comm'),
    ]
    faculty = models.CharField(max_length=20, choices=FACULTY_CHOICES, default='Not specified')

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Like(models.Model):
    liker = models.ForeignKey(User, related_name='likes_given', on_delete=models.CASCADE)
    liked = models.ForeignKey(User, related_name='likes_received', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('liker', 'liked')

    def __str__(self):
        return f"{self.liker.username} liked {self.liked.username}"

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    # add your fields here

from django.db import models
from django.contrib.auth.models import User

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=255)  # e.g., 'chat_admin_shaarvin'

    class Meta:
        ordering = ['timestamp']

class Dislike(models.Model):
    disliker = models.ForeignKey(User, related_name='dislikes_given', on_delete=models.CASCADE)
    disliked = models.ForeignKey(User, related_name='dislikes_received', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('disliker', 'disliked')

    def __str__(self):
        return f"{self.disliker.username} disliked {self.disliked.username}"

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('mood', 'Mood'),
        ('studies', 'Studies'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='mood')
    created_at = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} replied"

