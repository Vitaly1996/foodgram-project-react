from django.urls import include, path
from api.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = 'api'

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]