import csv
import os

from django.core.management.base import BaseCommand
from recipes.models import Ingredient

STATIC_DATA = 'home/admin/data'
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
