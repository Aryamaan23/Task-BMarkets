from django.core.management.base import BaseCommand
from datetime import datetime
from kbapp.models import AMCFund
import json

path='/Users/aryamaanpandey/Task-BMarkets/BmarketNew/kbapp/amcfundscheme.json'

class Command(BaseCommand):
     help = 'Stores fund data in the amcfund model'

     def handle(self,*args,**options):
         logic(path)
         self.stdout.write("Successfully created bank records")




def logic(path):
     pass