from api.tags_api.serializers import TagSerializer
from django.core.exceptions import ValidationError
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (FavoriteRecipe, IngredientInRecipe, Recipe,
                            ShoppingList)
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from tags.models import Tag


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиентов в рецепте."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Отображение полной информации о рецепте."""
    tags = TagSerializer(read_only=False, many=True)
    author = UserSerializer(read_only=True, many=False)
    image = Base64ImageField()
    ingredients = IngredientInRecipeSerializer(
        many=True,
        source='recipe_ingredient'
    )
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.favorites.filter(user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.shopping_list.filter(user=request.user).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Создание рецепта."""
    ingredients = IngredientInRecipeSerializer(
        many=True,
        read_only=True,
        source='recipe_ingredient'
    )
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField()

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

    def validate_ingredients(self, ingredients):
        ing = self.initial_data.get('ingredients')
        ingredients_list = []
        if not ing:
            raise serializers.ValidationError('Отсутствуют ингредиенты')
        for ingredient in ing:
            if ingredient['id'] in ingredients_list:
                raise ValidationError('Ингридиенты не могут повторяться')
            ingredients_list.append(ingredient['id'])
        return ingredients

    def validate_tags(self, tags):
        for tag in tags:
            if not Tag.objects.filter(id=tag.id).exists():
                raise ValidationError('Тега не существует')
        return tags

    @staticmethod
    def create_ingredients(recipe, ingredients):
        recipe_ingredients = [
            IngredientInRecipe(
                ingredient_id=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(
            recipe_ingredients,
            ignore_conflicts=True
        )

    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, self.initial_data['ingredients'])
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        instance.tags.set(validated_data.pop('tags'))
        self.create_ingredients(instance, self.initial_data['ingredients'])
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для короткого отображения рецепта."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов."""
    class Meta:
        model = FavoriteRecipe
        fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        user = data['user']
        if user.favorites.filter(recipe=data['recipe']).exists():
            raise ValidationError(
                'Рецепт уже в избранном.'
            )
        return data

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""
    class Meta:
        model = ShoppingList
        fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        user = data['user']
        if user.shopping_list.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в корзину'
            )
        return data

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
