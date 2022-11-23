import csv
import os

from django.core.management.base import BaseCommand
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient

STATIC_DATA = os.path.dirname(BASE_DIR) + r'/data'
INGREDIENT_FILE = STATIC_DATA + r'/ingredients.csv'


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(INGREDIENT_FILE) as f:
            reader = csv.reader(f)
            next(reader, None)
            ingredient_list = [
                Ingredient(
                    name=row[0],
                    measurement_unit=row[1]) for row in reader]
            Ingredient.objects.bulk_create(ingredient_list)
