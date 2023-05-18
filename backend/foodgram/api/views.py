from .serializers import TagSerializer, RecipeSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import User

from recipes.models import Tag, Recipe 


class TagViewSet(ReadOnlyModelViewSet):
    """Работа с тэгами."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class RecipeViewSet(ModelViewSet):
    """Работа с рецептами."""
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer