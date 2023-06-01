from django.contrib import admin

from .models import Tag


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
