from django.test import TestCase
from core import models


def sample_ingredient(name='rice'):
    return models.Ingredient.objects.create(name=name)


class RecipeTests(TestCase):

    def test_a_simple_recipe_string_representation(self):
        # Given / When
        recipe = models.Recipe.objects.create(
            name='Sea food paella',
            description='''Boil the rice in tasty stock.
                          Add vegatables after 10 minutes,
                          cover and add the seafood after that''',
        )

        # Then
        self.assertEquals(str(recipe), recipe.name)

    def test_a_recipe_with_ingredient_creates_an_ingredientForARecipe(self):
        # Given / When
        recipe = models.Recipe.objects.create(
            name='Sea food paella',
            description='''Boil the rice in tasty stock.
                          Add vegatables after 10 minutes,
                          cover and add the seafood after that''',
        )
        recipe.ingredients.add(sample_ingredient())

        # Then
        exists = models.IngredientForARecipe.objects.filter(
            Recipe=recipe
        ).exists()
        self.assertTrue(exists)
