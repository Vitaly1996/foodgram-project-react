import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from recipes.models import *
from users.serializers import UserSerializer
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


class TagSerializer(serializers.ModelSerializer):
    "Сериализатор для модели Tag только для чтения данных"
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    "Сериализатор для вспомогательной модели IngredientRecipe"
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    "Сериализатор для модели Recipe для чтения и записи данных"
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True, read_only=True)
    image = Base64ImageField(required=True, allow_null=True)
    tags = TagSerializer(many=True)

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        read_only_fields = ('author',)


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField(required=True, allow_null=True)

    def create_ingredients(self, ingredients):
        list_ingredients = [
            IngredientRecipe(
                ingredient=Ingredient.objects.get(ingredient['id']),
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        return IngredientRecipe.objects.bulk_create(list_ingredients)


    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients)
        return recipe


    def update(self, instance, validated_data):
        IngredientRecipe.objects.filter(recipe=instance).delete()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.set(tags)
        self.create_ingredients(
            ingredients=ingredients,
            recipe=instance
        )
        return super().update(instance=instance,
                              validated_data=validated_data)


    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )




# class ShoppingCartSerSerializer(serializers.ModelSerializer):
#     "Сериализатор для списка покупок"
#     recipe = RecipeSerializer
#
#     class Meta:
#         model = ShoppingCart
#         fields = ('recipe',)
