# Generated by Django 3.2.16 on 2023-06-03 18:31

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название тега', max_length=200, verbose_name='Название тега')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', help_text='Выберите цвет', image_field=None, max_length=7, samples=None, unique=True, verbose_name='HEX-код цвета')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
    ]
