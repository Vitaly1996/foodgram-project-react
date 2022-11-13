from api.views import *
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = 'api'

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]