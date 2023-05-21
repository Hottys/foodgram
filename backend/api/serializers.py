from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password
from djoser.serializers import UserCreateSerializer, UserSerializer


from recipes.models import Tag, Recipe, Ingredient
from users.models import User, Subscribe

class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""
    class Meta:
        model = Tag
        fields = '__all__'


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
        fields = '__all__'

class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор для cоздания пользователя."""
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Unable to create user with username me.'
            )
        return value


class UserSerializer(UserCreateSerializer):

    is_subscribed = serializers.SerializerMethodField()

    """Сериализатор для пользователя."""
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.following.filter(user=request.user).exists()