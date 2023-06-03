from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import Subscribe, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админ-панель управления пользователями."""
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('email', 'username')
    empty_value_display = ('-пусто-')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2'
            ),
        }),
    )


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Админ-панель управления подписками."""
    list_display = (
        'id',
        'user',
        'author'
    )
    empty_value_display = ('-пусто-')
