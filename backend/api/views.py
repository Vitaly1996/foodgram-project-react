from rest_framework import viewsets

from api.serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Ingredient.Только читает данные. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
