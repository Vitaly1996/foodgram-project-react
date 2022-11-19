from recipes.models import Recipe
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


def add_to(self, model, user, pk):
    """Метод для добавления"""
    if model.objects.filter(user=user, recipe__id=pk).exists():
        return Response({'error': 'Рецепт уже добавлен'},
                         status=status.HTTP_400_BAD_REQUEST
        )
    recipe = get_object_or_404(Recipe, pk=pk)
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


def download_cart(list_ing):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.setLineWidth(.3)
    c.setFont('Helvetica', 20)

    c.drawString(30, 750, 'Foodgram')
    c.drawString(30, 735, 'Ваш продуктовый помошник')
    c.line(30, 730, 580, 730)

    c.drawString(30, 710, 'Список покупок')
    val = 680
    for step, ing in enumerate(list_ing):
        ingredient = list(ing.values())
        product = ingredient[0]
        unit = ingredient[1]
        amount = ingredient[2]
        string = f'{step+1}. {product} {unit} - {amount}'
        c.drawString(30, val, string)
        val -= 20

    c.showPage()
    c.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='shoppcart_list.pdf'
    )