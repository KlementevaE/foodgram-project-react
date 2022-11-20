from django.core.management.base import BaseCommand

import csv
import os


from foodgram.settings import BASE_DIR
from recipes.models import Ingredient


STATIC_DATA = os.path.dirname(BASE_DIR) + r'/data'


INGREDIENT_FILE = STATIC_DATA + r'/ingredients.csv'


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(INGREDIENT_FILE) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                _, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )
