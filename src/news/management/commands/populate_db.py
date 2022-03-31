from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from src.news.models import ScrapConfig
class Command(BaseCommand):
    help = 'Populates the database with some testing data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Started database population process...'))
        if ScrapConfig.objects.filter().exists():
            self.stdout.write(self.style.SUCCESS('Database has already been populated. Cancelling the operation.'))
            return

        # Create users
        ScrapConfig.objects.create()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database.'))