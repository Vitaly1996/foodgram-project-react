import django_filters
from django_filters import rest_framework
from recipes.models import Ingredient, Recipe


class RecipeFilter(rest_framework.FilterSet):
    """Кастомный фильтр для модели Recipe"""
    is_favorited = django_filters.NumberFilter(
        method='get_is_favorited'
    )
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='get_is_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'author', 'tags', 'is_in_shopping_cart', ]

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(recipe_favourite__user_id=user.id)
        return queryset.all()

    def get_is_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(recipe_shopping_cart__user_id=user.id)
        return queryset.all()


class IngredientFilter(rest_framework.FilterSet):
    """Кастомный фильтр для модели Ingredient для имени"""
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ['name', ]
