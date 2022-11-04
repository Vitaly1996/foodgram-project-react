from rest_framework import serializers
from recipes.models import *


class IngredientSerializer(serializers.ModelSerializer):
    "Сериализатор для модели Ingredient только для чтения данных"
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        lookup_field = 'name'


class TagSerializer(serializers.ModelSerializer):
    "Сериализатор для модели Tag только для чтения данных"
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

