from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse("recipe:recipe-list")


def sample_recipe(**params):
    """Create and return a sample recipe"""

    defaults = {
        'name': 'Toast',
        'description': 'Put bread in a toaster',
    }
    defaults.update(params)

    return Recipe.objects.create(**defaults)


class PublicRecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_should_retrieve_recipe_list(self):
        # Given
        sample_recipe()
        sample_recipe()

        """When"""
        res = self.client.get(RECIPES_URL)

        # Then
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_should_create_a_recipe_with_ingredients(self):
        # Given
        payload = {
            'name': 'Chocolate fudge cake',
            'description': 'Mix the chocolate with the fudge and the cake',
            'ingredients': [
                {'name': 'dough'},
                {'name': 'cheese'},
                {'name': 'tomato'}
            ]
        }

        # When
        res = self.client.post(RECIPES_URL, payload, format='json')

        # Then
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEqual(payload['name'], getattr(recipe, 'name'))
        self.assertEqual(payload['description'],
                         getattr(recipe, 'description'))

        for i in range(len(res.data['ingredients'])):
            self.assertEqual(payload['ingredients'][i]['name'],
                             res.data['ingredients'][i]['name'])
