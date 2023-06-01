# Generated by Django 3.2.16 on 2023-06-01 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
        ('recipes', '0003_auto_20230601_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ingredients.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Выберите ингредиенты', related_name='recipes', through='recipes.IngredientInRecipe', to='ingredients.Ingredient', verbose_name='Ингредиенты в рецепте'),
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
    ]
