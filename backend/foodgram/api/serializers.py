from rest_framework import serializers
from djoser.serializers import UserSerializer
from rest_framework.serializers import ModelSerializer

from recipes.models import Tag, Recipe, Ingredient
from users.models import User

class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиентов."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )

class UserSerializer(UserSerializer):
    """Сериализатор для пользователя."""
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', ) #'is_subscribed'