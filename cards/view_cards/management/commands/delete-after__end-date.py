from django.core.management.base import BaseCommand
from view_cards.models import Card
import datetime

class Command(BaseCommand):
    help = 'Delete cards with overdue activity'

    def handle(self, *args, **kwargs):
        now = datetime.datetime.now()
        for card in Card.objects.all():
            if now > card.activity_end_date:
                card.delete()
        self.stdout.write(f"Прострочені картки було видалено")