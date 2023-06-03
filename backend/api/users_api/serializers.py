import re

from django.core.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from users.models import User


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

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise ValidationError(
                {'Имя пользователя не может быть <me>.'})
        if re.search(
            r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', data['username']
        ) is None:
            raise ValidationError(
                ('Недопустимые символы в username'),
            )
        return data


class UserSerializer(UserSerializer):
    """Сериализатор для пользователя."""

    is_subscribed = serializers.SerializerMethodField()

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
        return obj.subscribing.filter(user=request.user).exists()


class SubscribeRecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для короткого отображения рецепта."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscribeSerializer(UserSerializer):
    """Сериализатор для подписок."""
    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        author = obj.recipes.all()
        return SubscribeRecipeShortSerializer(author, many=True).data

    def get_recipes_count(self, obj):
        return obj.subscribing.count()
