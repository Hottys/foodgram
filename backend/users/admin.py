from django.contrib import admin

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админ-панель управления пользователями."""
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('email', 'username')
    empty_value_display = ('-пусто-')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Админ-панель управления подписками."""
    list_display = (
        'id', 
        'user', 
        'author'
    )
    list_filter = ('user', 'author')
    empty_value_display = ('-пусто-')