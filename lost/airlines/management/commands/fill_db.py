from django.core.management.base import BaseCommand
from airlines.models import Airlines
from django.db.models import Q
import os
import json
from datetime import datetime


JSON_PATH = 'airlines/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        airlines = load_from_json('airlines_lost_2018')

        for airline in airlines:
            air_query_set = (Q(title=airline['title']))
            count_company = Airlines.objects.filter(air_query_set).count()
            if count_company < 1:
                new_airline = Airlines(**airline)
                new_airline.save()
            else:
                compare_query_set = (Q(title=airline['title']) & Q(country=airline['country']) & Q(status=airline['status']))
                does_not_match = Airlines.objects.filter(compare_query_set).count()
                edit_airlines_set = (Q(title=airline['title']))
                edit_airlines = Airlines.objects.get(edit_airlines_set)
                if does_not_match < 1:
                    edit_airlines.changed = datetime.datetime.now().replace(microsecond=0).isoformat()
                    edit_airlines.country = airline['country']
                    edit_airlines.status = airline['status']
                    edit_airlines.save()
