from recipes.models import Favourite, Recipe, ShoppingCart
from rest_framework import status
from rest_framework.response import Response


def add_to(self, request, model, user, pk):
    """Метод для добавления"""
    if model.objects.filter(user=user, recipe__id=pk).exitst():
        return Response({'error': 'Рецепт уже добавлен'},
                         status=status.HTTP_400_BAD_REQUEST
        )
    recipe = Recipe.objects.get_object_or_404(pk=pk)
    instance = model.objects.create(user=user, recipe=recipe)
    serializer = self.get_serializer(instance)
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def delete_from(self, model, user, pk):
    """Метод для удаления"""
    if model.objects.filter(user=user, recipe__id=pk).exists():
        model.objects.filter(
            user=user, recipe__id=pk
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
