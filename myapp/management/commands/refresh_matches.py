from django.core.management.base import BaseCommand
from myapp.models import Like, Dislike

class Command(BaseCommand):
    help = 'Deletes all Like and Dislike records (refreshes match history for all users)'

    def handle(self, *args, **kwargs):
        Like.objects.all().delete()
        Dislike.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All match history (likes and dislikes) has been cleared.'))
