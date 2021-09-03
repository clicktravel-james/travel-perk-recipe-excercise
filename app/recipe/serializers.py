from rest_framework import serializers
from core.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for an ingredient object"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientRecipeDetailsSerializer(serializers.ModelSerializer):
    """Serializer for an ingredient object"""

    class Meta:
        model = Ingredient
        read_only_fields = ('id',)
        exclude = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for an recipe object"""
    ingredients = IngredientRecipeDetailsSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients',)
        read_only_fields = ('id',)

    def map_to_ingredient_name(self, ingredients_object):
        if ingredients_object and ingredients_object['name']:
            return ingredients_object['name']

        return None

    def create(self, validated_data):
        """Parse the correct values from the request and
        pass them to the model"""
        name = validated_data['name']
        description = validated_data['description']
        ingredient_names = map(self.map_to_ingredient_name,
                               validated_data['ingredients'])

        return Recipe.objects.create_recipe_with_ingredients(name,
                                                             description,
                                                             ingredient_names)

    def update(self, instance, validated_data):
        """Deal specifically with the nested ingredients then call super
        for auto-magically dealing with the supported basic fields"""
        if 'ingredients' in validated_data:
            ingredient_data = validated_data.pop('ingredients')
            ingredient_names = map(self.map_to_ingredient_name,
                                   ingredient_data)
            Recipe.objects.update_recipe_ingredients(
                recipe_instance=instance,
                ingredient_names=ingredient_names,
            )

        return super().update(instance, validated_data)
