from django.contrib import admin
from .models import Ingredient


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
