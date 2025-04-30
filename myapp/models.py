from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    self_bio = models.TextField(default="No bio available")
    profile_picture = models.ImageField(upload_to="author_images/", null=True, blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

        