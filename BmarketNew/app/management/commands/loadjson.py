from app.models import Bank
import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Loads data from JSON file into amc model'

    def handle(self, *args, **kwargs):
        with open('/Users/aryamaanpandey/Task-BMarkets/BmarketNew/app/load.json') as f:
            data = json.load(f)
        
        bank_obj = Bank(**data['fields'])
        bank_obj.save()