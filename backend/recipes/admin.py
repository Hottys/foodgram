from django.contrib import admin

from .models import (Ingredient, Tag, Recipe,
                     IngredientInRecipe, FavoriteRecipe, ShoppingList)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админ-панель управления рецептами."""
    list_display = (
        'id',
        'author',
        'name',
        'cooking_time',
        'number_of_favorites'
    )
    list_filter = ('author', 'name', 'tags')
    empty_value_display = ('-пусто-')

    def number_of_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админ-панель управления ингредиентами."""
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)
    empty_value_display = ('-пусто-')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админ-панель управления тегами."""
    list_display = (
        'id',
        'name',
        'color',
        'slug'
    )
    empty_value_display = ('-пусто-')


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Админ-панель управления избранными рецептами."""
    list_display = (
        'id',
        'user',
        'recipe',
    )
    empty_value_display = ('-пусто-')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """Админ-панель управления списками покупок."""
    list_display = (
        'id',
        'user',
        'recipe',
    )
    empty_value_display = ('-пусто-')