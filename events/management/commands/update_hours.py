from django.core.management.base import BaseCommand
from events.models import WorkShift

class Command(BaseCommand):
    help = 'Update hours field to 10'

    def handle(self, *args, **kwargs):
        WorkShift.objects.update(hours=10)