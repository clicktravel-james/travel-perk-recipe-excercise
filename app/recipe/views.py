from rest_framework import viewsets, mixins
from core.models import Ingredient
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
        return queryset.order_by('-name').distinct()
