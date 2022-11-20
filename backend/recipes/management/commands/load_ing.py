import json
import os

from django.core.management.base import BaseCommand

from foodgram.settings import BASE_DIR
from recipes.models import Ingredient

INGREDIENT_JSON = 'ingredients.json'
DATA_PATH = os.path.join(BASE_DIR, '..', 'data')


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.join(DATA_PATH, INGREDIENT_JSON)
        Ingredient.objects.all().delete()

        with open(path, 'r', encoding='utf-8') as file:
            reader = json.load(file)
            Ingredient.objects.bulk_create([
                Ingredient(**x) for x in reader
            ])
