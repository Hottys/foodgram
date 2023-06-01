from colorfield.fields import ColorField
from django.db import models


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        help_text='Название тега',
    )
    color = ColorField(
        format='hex',
        max_length=7,
        unique=True,
        help_text='Выберите цвет',
        verbose_name='HEX-код цвета',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Адрес',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
