from django.test import TestCase
from django.urls import reverse
from django.db.models import Q

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Recipe, Ingredient

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


def create_recipe_details_url(recipe_id):
    """Function for creating a dynamic url for recipe details"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def map_ingredient_model_to_name(ingredients_model):
    if ingredients_model and ingredients_model.name:
        return ingredients_model.name

    return None


def map_ingredient_data_to_name(ingredients_object):
    if ingredients_object and ingredients_object['name']:
        return ingredients_object['name']

    return None


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

    def test_should_partially_update_a_recipe_with_basic_details(self):
        # Given
        original_recipe = sample_recipe()
        payload = {
            'name': 'Chocolate fudge cake',
            'description': 'Mix the chocolate with the fudge and the cake',
        }
        recipe_details_url = create_recipe_details_url(original_recipe.id)

        # When
        res = self.client.patch(recipe_details_url, payload, format='json')

        # Then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEqual(payload['name'], getattr(recipe, 'name'))
        self.assertEqual(payload['description'],
                         getattr(recipe, 'description'))

    def test_should_partially_update_a_recipe_with_ingredients(self):
        # Given
        original_recipe = sample_recipe()
        original_recipe.ingredients.create(name="pepperoni")
        payload = {
            'ingredients': [
                {'name': 'dough'},
                {'name': 'cheese'},
                {'name': 'tomato'}
            ]
        }
        recipe_details_url = create_recipe_details_url(original_recipe.id)

        # When
        res = self.client.patch(recipe_details_url, payload, format='json')

        # Then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEqual(res.data['name'], getattr(recipe, 'name'))
        self.assertEqual(res.data['description'],
                         getattr(recipe, 'description'))

        all_persisted_ingredients_for_recipe = recipe.ingredients.all()
        ingredient_model_names = map(map_ingredient_model_to_name,
                                     all_persisted_ingredients_for_recipe)
        ingredient_response_names = map(map_ingredient_data_to_name,
                                        res.data['ingredients'])
        self.assertEqual(
            set(ingredient_model_names),
            set(ingredient_response_names)
        )

    def test_should_delete_a_recipe_with_its_ingredients(self):
        # Given
        recipe = sample_recipe()
        Ingredient1 = recipe.ingredients.create(name="pepperoni")
        Ingredient2 = recipe.ingredients.create(name="cheese")
        recipe_details_url = create_recipe_details_url(recipe.id)

        # When
        res = self.client.delete(recipe_details_url,)

        # Then
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        recipe = Recipe.objects.filter(id=recipe.id)
        self.assertEqual(len(recipe), 0)
        persisted_ingredients = Ingredient.objects.filter(
            Q(id=Ingredient1.id) | Q(id=Ingredient2.id)
        )
        self.assertEqual(len(persisted_ingredients), 0)
