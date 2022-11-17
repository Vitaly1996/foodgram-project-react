from api.views import *
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import *

router = DefaultRouter()

app_name = 'api'

router.register('users', UsersViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]