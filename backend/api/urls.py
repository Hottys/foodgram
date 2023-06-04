from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.ingredients_api.views import IngredientViewSet
from api.recipes_api.views import RecipeViewSet
from api.tags_api.views import TagViewSet
from api.users_api.views import UserViewSet

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
