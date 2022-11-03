from django.contrib.auth import get_user_model
from django.db import models
from colorfield import fields

from foodgram.settings import MAX_LENGTH

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = fields.ColorField(max_length=7, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self)-> str:
        return self.name[:MAX_LENGTH]


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=200, verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self)-> str:
        return self.name[:MAX_LENGTH]


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    cooking_time = models.DurationField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes_author'
    )
    ingredients = models.ManyToManyField("IngredientRecipe")
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self)-> str:
        return self.name[:MAX_LENGTH]


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class Follow(models.Model):
    pass




