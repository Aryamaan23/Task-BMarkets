"/Users/aryamaanpandey/Desktop"
import csv
from django.core.management.base import BaseCommand
from app.models import Bank


class Command(BaseCommand):
    help = 'Loads data from a CSV file into the Bank model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                bank, created = Bank.objects.get_or_create(
                    bank_id=row['bank_id'],
                    defaults={
                        'bank_id':row['bank_id'],
                        'bank_name': row['bank_name'],
                        'bank_website': row['bank_website'],
                        'bank_number': row['bank_number'],
                        'bank_logo': row['bank_logo']
                    }
                )
                if not created:
                    bank.bank_id=row['bank_id']
                    bank.bank_name = row['bank_name']
                    bank.bank_website = row['bank_website']
                    bank.bank_number = row['bank_number']
                    bank.bank_logo = row['bank_logo']
                    bank.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))
