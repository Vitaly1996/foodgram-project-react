from rest_framework import serializers
from recipes.models import *


class IngredientSerializer(serializers.ModelSerializer):
    "Сериализатор для модели Ingredient только для чтения данных"
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        lookup_field = 'name'
