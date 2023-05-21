from .serializers import TagSerializer, RecipeSerializer, IngredientSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from djoser.views import UserViewSet

from recipes.models import Tag, Recipe, Ingredient
from users.models import User

class TagViewSet(ReadOnlyModelViewSet):
    """Работа с тэгами."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (IsAdminOrReadOnly,)

class IngredientViewSet(ModelViewSet):
    """Работа с ингридиентами"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # permission_classes = (IsAdminOrReadOnly,)

class RecipeViewSet(ModelViewSet):
    """Работа с рецептами."""
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer

class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer