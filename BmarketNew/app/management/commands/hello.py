from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help='Displays hello.'

    def handle(self, *args, **options):
        self.stdout.write("Hello World!")

        
        