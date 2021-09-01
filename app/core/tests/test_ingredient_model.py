from django.test import TestCase
from core import models


class IngredientModelTests(TestCase):
    def test_the_ingredient_string_rep(self):
        # Given / When
        ingredient = models.Ingredient.objects.create(
            name='Becon'
        )

        # Then
        self.assertEquals(str(ingredient), ingredient.name)
