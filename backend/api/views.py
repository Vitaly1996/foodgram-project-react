from api.pagination import CustomPagination
from api.serializers import *
from api.utils import add_to, delete_from
from users.permissions import AuthorOrReadOnly
from recipes.models import *
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Ingredient.Только читает данные. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


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
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('color', 'birth_year')
    pagination_class = CustomPagination
    permission_classes = (AuthorOrReadOnly, )

    def perform_create(self, serializer):
        """Передает в поле author данные о пользователе. """
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Переопределение выбора сериализатора"""
        if self.action in ('retrieve', 'list'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path=r'(?P<recipe>\d+)/shopping_cart',
        url_name='recipe_shopping_cart',
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """Метод для добавления/удаления из список покупок"""
        if request.method == 'POST':
            return add_to(ShoppingCart, request.user, pk)
        else:
            return delete_from(ShoppingCart, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path=r'(?P<recipe>\d+)/favorite',
        url_name='recipe_favorite',
        permission_classes=[permissions.IsAuthenticated]
    )
    def favourite(self, request, pk):
        """Метод для добавления/удаления из избранного"""
        if request.method == 'POST':
            return add_to(Favourite, request.user, pk)
        else:
            return delete_from(Favourite, request.user, pk)
