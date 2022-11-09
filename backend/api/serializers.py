import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from recipes.models import *
import webcolors


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


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
        fields = ('id', 'name', 'color', 'slug',)


class RecipeSerializer(serializers.ModelSerializer):
    "Сериализатор для модели Recipe для чтения и записи данных"
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_car = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    ingredients = IngredientSerializer(many=True,)
    color = Hex2NameColor()
    image = Base64ImageField(required=False, allow_null=True)

    # def create(self, validated_data):
    #     return IngredientRecipe.objects.create(**validated_data)

    def update(self):
        pass


    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_car(self, obj):
        return False

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)


class IngredientRecipe(serializers.ModelSerializer):
    "Сериализатор для вспомогательной модели IngredientRecipe."
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = ('ingredient', 'amount')

