from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.ingredients_api.serializers import IngredientSerializer
from ingredients.models import Ingredient


class IngredientViewSet(ReadOnlyModelViewSet):
    """Работа с ингридиентами."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = None
