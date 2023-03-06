"/Users/aryamaanpandey/Desktop"
import csv
from django.core.management.base import BaseCommand
from app.models import Bank


class Command(BaseCommand):
    help = 'Loads data from a CSV file into the Bank model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):

        """
        Get_or_create method tries to get a Bank object with the specified bank_id value from the database. If a Bank object with the specified bank_id does not exist, it creates a new Bank object using the specified defaults parameter as its attributes.
        The defaults parameter is a dictionary that specifies the default values for the attributes of the new Bank object. If a Bank object with the specified bank_id already exists in the database, the defaults parameter is ignored, and the existing Bank object is returned.
        """
        csv_file = options['csv_file']
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                bank, created = Bank.objects.get_or_create(
                    bank_id=row['bank_id'],
                    defaults={
                        'bank_name': row['bank_name'],
                        'bank_website': row['bank_website'],
                        'bank_number': row['bank_number'],
                        'bank_logo': row['bank_logo']
                    }
                )
                if created:
                     self.stdout.write(self.style.SUCCESS(f"Successfully created bank----> {bank.bank_name}."))
                else:
                    self.stdout.write(self.style.WARNING(f"Bank {bank.bank_name} already exists in the database. Skipping..."))
                    bank.bank_name = row['bank_name']
                    bank.bank_website = row['bank_website']
                    bank.bank_number = row['bank_number']
                    bank.bank_logo = row['bank_logo']
                    bank.save()

        #self.stdout.write(self.style.SUCCESS('Data imported successfully.'))

        
                
