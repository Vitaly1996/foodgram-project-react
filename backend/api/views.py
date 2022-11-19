from api.filters import IngredientSearchFilter, RecipeFilter
from api.pagination import CustomPagination
from api.serializers import *
from api.utils import add_to, delete_from, download_cart
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import *
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from users.permissions import AuthorOrReadOnly

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Ingredient.Только читает данные. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    # filter_backends = (filters.SearchFilter, DjangoFilterBackend, )
    filter_class = IngredientSearchFilter
    search_fields = ('^name',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Tag.Только читает данные. """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Recipe и для чтения и для записи. """
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend, )
    filter_class = RecipeFilter
    pagination_class = CustomPagination
    permission_classes = (AuthorOrReadOnly, )

    def perform_create(self, serializer):
        """Передает в поле author данные о пользователе. """
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Переопределение выбора сериализатора"""
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """Метод для добавления/удаления из список покупок"""
        if request.method == 'POST':
            return add_to(self, ShoppingCart, request.user, pk)
        else:
            return delete_from(self, ShoppingCart, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk):
        """Метод для добавления/удаления из избранного"""
        if request.method == 'POST':
            return add_to(self, Favourite, request.user, pk)
        else:
            return delete_from(self, Favourite, request.user, pk)

    # @action(
    #     detail=True,
    #     methods=['get'],
    #     permission_classes=[permissions.IsAuthenticated]
    # )
    # def download_shopping_cart(self, request):
    #     """Метод для добавления/удаления из избранного"""
    #     if request.method == 'POST':
    #         return add_to(self, Favourite, request.user, pk)
    #     else:
    #         return delete_from(self, Favourite, request.user, pk)


class DownloadCart(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        list_ing = request.user.user_shopping_cart.values(
            'recipe__ingredients__ingredient__name',
            'recipe__ingredients__ingredient__measurement_unit'
        ).order_by('recipe__ingredients__ingredient__name'
        ).annotate(summ_amount=Sum('recipe__ingredients__amount'))
        return download_cart(list_ing)

    # @classmethod
    # def get_extra_actions(cls):
    #     return []
