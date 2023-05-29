# Generated by Django 3.2.19 on 2023-05-29 05:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Количество не может быть меньше 1.'), django.core.validators.MaxValueValidator(100, message='Столько не скушать :) :)')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Время приготовление не может быть меньше 1 минуты.'), django.core.validators.MaxValueValidator(1440, message='Время приготовления - не больше 24 часов!')], verbose_name='Время приготовления (в минутах)'),
        ),
    ]