from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.ingredients_api.serializers import IngredientSerializer
from ingredients.models import Ingredient

from .filters import IngredientFilter


class IngredientViewSet(ReadOnlyModelViewSet):
    """Работа с ингридиентами."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None
