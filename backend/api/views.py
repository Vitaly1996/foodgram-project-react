from rest_framework import viewsets

from api.serializers import *
from recipes.models import *
from api.pagination import CustomPagination


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Ingredient.Только читает данные. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Tag.Только читает данные. """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Recipe и для чтения и для записи. """
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """Переопределение выбора сериализатора"""
        if self.action in ('retrieve', 'list'):
            return RecipeReadSerializer
        return RecipeWriteSerializer


