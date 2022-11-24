import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient

INGREDIENT_FILE = 'home/admin/data/ingredients.csv'


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
