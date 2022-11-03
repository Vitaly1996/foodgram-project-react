from django.urls import include, path
from api.views import IngredientViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = 'api'

router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]