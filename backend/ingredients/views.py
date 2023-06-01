from .models import Ingredient
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.serializers import IngredientSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    """Работа с ингридиентами."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = None
