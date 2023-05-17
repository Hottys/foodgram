from django.urls import include, path
from rest_framework.routers import DefaultRouter


v1_router = DefaultRouter()

v1_router.register('recipes', RecipeViewSet)
v1_router.register('ingredients', IngredientViewSet)
v1_router.register('tags', TagViewSet)

v1_urlpatterns = [
    path('', include(v1_router.urls)),
]