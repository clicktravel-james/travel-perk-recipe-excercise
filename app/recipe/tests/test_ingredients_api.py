from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse("recipe:ingredient-list")


class PublicIngredientsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_should_get_an_ingredient(self):
        # Given
        Ingredient.objects.create(name="Orange")
        Ingredient.objects.create(name="Salmon")

        # When
        res = self.client.get(INGREDIENTS_URL)

        # Then
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_ingredient_successful(self):
        # Given
        payload = {
            'name': 'This is a test ingredient'
        }

        # When
        self.client.post(INGREDIENTS_URL, payload)

        # Then
        exists = Ingredient.objects.filter(
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid_payload(self):
        # Given
        payload = {
            'name': ''
        }

        # When
        res = self.client.post(INGREDIENTS_URL, payload)

        # Then
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
