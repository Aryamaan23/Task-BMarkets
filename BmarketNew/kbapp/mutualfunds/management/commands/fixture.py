# from django.core.management import call_command
# from kbapp.models import Amc
# from django.core.management import BaseCommand, CommandError
# from django.core.management import call_command

# fixture_path = '/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/fixtures/amc.json'

# # Load the fixture data into the Amc model
# # Load the fixture data into the Amc model

# class Command(BaseCommand):
#     help = 'Loads data from json to db'
 
#     def handle(self, *args, **kwargs):
#         call_command('loaddata', fixture_path, verbosity=0)





# from django.core.management import BaseCommand, CommandError
# from django.core.management import call_command
# from kbapp.models import Amc
# import json
 
# # class Command(BaseCommand):
# #     help = 'Loads data from json to db'
 
# #     def handle(self, *args, **kwargs):
# #         call_command('loaddata','kbapp/amc_data.json')
 
# class Command(BaseCommand):
#     help = 'Loads data from amc.json fixture'
 
#     def handle(self, *args, **options):
#         call_command('loaddata', 'kbapp/fixtures/amc.json')

# from django.core.management import call_command
# from django.core.management.base import BaseCommand
# from kbapp.models import Amc

# class Command(BaseCommand):
#     help = 'Load data from a JSON fixture file into the Amc model'

#     def add_arguments(self, parser):
#         parser.add_argument('fixture_file', type=str, help='Path to the JSON fixture file')

#     def handle(self, *args, **options):
#         fixture_file = options['fixture_file']

#         # Load the fixture data into the Amc model
#         call_command('loaddata', fixture_file, verbosity=0)

#         self.stdout.write(self.style.SUCCESS('Successfully loaded data from JSON fixture file'))


from kbapp.models import Amc
import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Loads data from JSON file into amc model'

    def handle(self, *args, **kwargs):
        with open('/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/fixtures/amc.json') as f:
            data = json.load(f)
        
        bank_obj = Amc(**data['fields'])
        bank_obj.save()
