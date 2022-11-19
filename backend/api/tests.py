from django.test import TestCase
from django.urls import reverse
from recipes.models import (Tag,
                            Ingredient,)
from rest_framework import status
from rest_framework.test import APITestCase


class IngredientModelTest(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(
            name='Тестовое название',
            measurement_unit='кг'
        )

    def test_name(self):
        self.assertEqual(str(self.ingredient), self.ingredient.name)


class IngredientTests(APITestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(
            name='Тестовое название',
            measurement_unit='кг'
        )

    def check_object(self, data, obj):
        self.assertEqual(data.get('id'), obj.pk)
        self.assertEqual(data.get('name'), obj.name)
        self.assertEqual(data.get('measurement_unit'), obj.measurement_unit)

    def test_get_list(self):
        """
        Проверка правильности получения списка ингредиентов
        """
        url = reverse('api:ingredients-list')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_detail(self):
        """
        Проверка правильности получения одного ингредиента
        """
        url = reverse('api:ingredients-detail',
                      kwargs={'pk': self.ingredient.pk})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.check_object(resp.data, self.ingredient)


class TagTests(APITestCase):
    def setUp(self):
        self.tag = Tag.objects.create(
            name='Завтрак',
            color='#E26C2D',
            slug='breakfast',
        )

    def check_object(self, data, obj):
        self.assertEqual(data.get('id'), obj.pk)
        self.assertEqual(data.get('name'), obj.name)
        self.assertEqual(data.get('color'), obj.color)
        self.assertEqual(data.get('slug'), obj.slug)

    def test_get_list(self):
        """
        Проверка правильности получения списка тегов
        """
        url = reverse('api:tags-list')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_detail(self):
        """
        Проверка правильности получения одного тега
        """
        url = reverse('api:tags-detail',
                      kwargs={'pk': self.tag.pk})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.check_object(resp.data, self.tag)
