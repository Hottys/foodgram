from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'login',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('email', 'login')
    search_fields = ('login',)
    empty_value_display = ('-пусто-')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_filter = ('user', 'author')
    search_fields = ('author',)
    empty_value_display = ('-пусто-')