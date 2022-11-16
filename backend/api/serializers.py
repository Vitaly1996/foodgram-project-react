import base64

import webcolors
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from recipes.models import *
from rest_framework import serializers
from users.serializers import UserSerializer


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
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True, read_only=True)
    image = Base64ImageField(required=True, allow_null=True)
    tags = TagSerializer(many=True)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        favorite = request.user.user_favourite.filter(recipe=obj)
        return favorite.exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        shopping_cart = request.user.user_shopping_cart.filter(recipe=obj)
        return shopping_cart.exists()

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
    ingredients = IngredientRecipeSerializer(many=True)

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient.objects.filter(id=ingredient['id'])
            )
            ing, _ = IngredientRecipe.objects.get_or_create(
                ingredient=current_ingredient,
                amount=ingredient['amount']
            )
            recipe.ingredients.add(ing)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.save()
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, recipe, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            recipe.ingredients.clear()
            self.create_ingredients(ingredients, recipe)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            recipe.tags.set(tags_data)
        return super().update(
            instance=recipe,
            validated_data=validated_data
        )

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


class RecipeShortInfo(serializers.ModelSerializer):
    """"Сериализатор рецептов  для отображения нужных полей"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerSerializer(serializers.ModelSerializer):
    "Сериализатор для списка покупок"

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')


class Favourite(serializers.ModelSerializer):
    "Сериализатор для списка покупок"

    class Meta:
        model = Favourite
        fields = ('id', 'name', 'image', 'cooking_time')
