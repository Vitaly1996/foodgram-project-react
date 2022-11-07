from rest_framework import viewsets

from api.serializers import *
from recipes.models import *


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Ingredient.Только читает данные. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Tag.Только читает данные. """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Recipe и для чтения и для записи. """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')