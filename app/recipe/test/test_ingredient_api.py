from rest_framework import status
from rest_framework.test import APIClient

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')

def get_ingredient_url(id):
    return reverse('recipe:ingredient-detail', args=[id])

def create_uers(email='test@example.com', password='pasaseqweg'):
    return get_user_model().objects.create_user(email=email, password=password)

class PublicIngredient(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredient(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_uers()
        self.client.force_authenticate(self.user)

    def test_auth_required(self):
        Ingredient.objects.create(user=self.user, name='Kela')
        Ingredient.objects.create(user=self.user, name='Coco')

        res = self.client.get(INGREDIENT_URL)

        inredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(inredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        user2 = create_uers(email='test2@example.com')
        Ingredient.objects.create(user=user2, name='somting')
        ingredient = Ingredient.objects.create(user=self.user, name='somone')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test__update_ingredients(self):
        ingredient = Ingredient.objects.create(user=self.user, name='test_update')

        payload = {'name': 'test_updateed'}
        url = get_ingredient_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user, name='tset_delete')

        url = get_ingredient_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())