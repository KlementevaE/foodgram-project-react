from django.core.management.base import BaseCommand

import csv
import os


from foodgram.settings import BASE_DIR
from recipes.models import Ingredient


STATIC_DATA = os.path.dirname(BASE_DIR) + r'/data'


INGREDIENT_FILE = STATIC_DATA + r'/ingredients.csv'


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        ingredient_list = []
        with open(INGREDIENT_FILE) as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                name = row[0],
                measurement_unit = row[1],
                new_ingredient = Ingredient(
                    name=name,
                    measurement_unit=measurement_unit),
                ingredient_list.append(new_ingredient)
            Ingredient.objects.bulk_create(ingredient_list)
