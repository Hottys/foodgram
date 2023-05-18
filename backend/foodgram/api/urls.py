from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, RecipeViewSet

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet, 'recipes')


urlpatterns = [
    path('', include(router.urls)),
]