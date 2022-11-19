import django_filters
from recipes.models import Recipe, Ingredient
from rest_framework.filters import SearchFilter


class RecipeFilter(django_filters.rest_framework.FilterSet):
    """Кастомный фильтр для модели Recipe"""
    is_favorited = django_filters.NumberFilter(
        method='get_is_favorited'
    )
    author = django_filters.CharFilter(
        field_name='author__username', lookup_expr='icontains'
    )
    tags = django_filters.CharFilter(
        field_name='tags__slug', lookup_expr='icontains'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='get_is_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'author', 'tags', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, value):
        user = self.request.user
        if value == 1:
            if user.is_authenticated:
                return queryset.filter(user_favourite__user_id=user.id)
        return queryset.all()

    def get_is_shopping_cart(self, queryset, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(user_shopping_cart__user_id=user.id)
        return queryset.all()


class IngredientSearchFilter(SearchFilter):
    """Кастомный фильтр для модели Ingredient для имени"""
    search_param = 'name'
