from django.core.management.base import BaseCommand
from myapp.models import Message

class Command(BaseCommand):
    help = 'Deletes all chat messages (clears chat history for all users)'

    def handle(self, *args, **kwargs):
        Message.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All chat history has been cleared.'))
