from django_filters import rest_framework as filters
from recipes.models import Ingredient


class IngredientRangeFilter(filters.FilterSet):
    min_number = filters.NumericRangeFilter(field_name="number", lookup_expr='gte')
    max_number = filters.NumericRangeFilter(field_name="number", lookup_expr='lte')

    class Meta:
        model = Ingredient
        fields = ['title']