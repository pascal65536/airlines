from django.core.management.base import BaseCommand
from airlines.models import Airlines

from django.contrib.auth.models import User

import os
import json

JSON_PATH = 'airlines/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8-sig') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        airlines = load_from_json('airlines_lost_2018')

        Airlines.objects.all().delete()

        for airline in airlines:
            print(airline)
            new_airline = Airlines(**airline)
            new_airline.save()

        User.objects.all().delete()
        User.objects.create_superuser(username='1', email='raz@dva.tri', password='1')
