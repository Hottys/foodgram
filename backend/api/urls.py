from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import RecipeViewSet
from users.views import UserViewSet
from tags.views import TagViewSet
from ingredients.views import IngredientViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
