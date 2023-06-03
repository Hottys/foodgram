from django.contrib import admin

from .models import FavoriteRecipe, IngredientInRecipe, Recipe, ShoppingList


class IngredientInline(admin.TabularInline):
    model = IngredientInRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админ-панель управления рецептами."""
    list_display = (
        'id',
        'author',
        'name',
        'cooking_time',
        'pub_date',
        'number_of_favorites'
    )
    list_filter = ('author', 'name', 'tags')
    filter_horizontal = ('tags',)
    inlines = [
        IngredientInline,
    ]
    empty_value_display = ('-пусто-')

    @admin.display(description='Количество добавлений в избранное')
    def number_of_favorites(self, obj):
        return obj.favorites.count()


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


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    """Админ-панель управления ингредиентами в рецептах."""
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    empty_value_display = ('-пусто-')
