import csv

from django.core.management.base import BaseCommand
from django.conf import settings
from recipes.models import Ingredient


STATIC_DATA = settings.BASE_DIR


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(f'{STATIC_DATA}/data/ingredients.csv') as f:
            reader = csv.reader(f)
            next(reader, None)
            ingredient_list = [
                Ingredient(
                    name=row[0],
                    measurement_unit=row[1]) for row in reader]
            Ingredient.objects.bulk_create(ingredient_list)
