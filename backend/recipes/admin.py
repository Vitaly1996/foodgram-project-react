from django.contrib import admin
from recipes.models import *
from users.models import User, Follow


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    empty_value_display = '-пусто-'
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'image', 'cooking_time', 'author',)
    list_filter = ('author', 'tags',)
    empty_value_display = '-пусто-'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount',)
    empty_value_display = '-пусто-'


# @admin.register(ShoppingCart)
# class ShoppingCartAdmin(admin.ModelAdmin):
#     list_display = ('user__username', 'recipe__name',)
#     empty_value_display = '-пусто-'
#
#
# @admin.register(Follow)
# class FollowAdmin(admin.ModelAdmin):
#     list_display = ('user__username', 'recipe__name',)
#     empty_value_display = '-пусто-'

admin.site.register(ShoppingCart)
admin.site.register(Follow)
admin.site.register(Favourite)
admin.site.register(User)
