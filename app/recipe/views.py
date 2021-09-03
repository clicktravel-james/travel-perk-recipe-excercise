from rest_framework import viewsets, mixins
from core.models import Ingredient, Recipe
from recipe import serializers


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """Manage ingredients in the database"""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """Return Ingredients objects ordered by name"""
        queryset = self.queryset
        return queryset.order_by('-id').distinct()


class RecipeViewSet(viewsets.ModelViewSet,):
    """Manage Recipe in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Return recipes for the current authenticated user only"""
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.order_by('-id')
