# Generated by Django 3.2.16 on 2023-06-03 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_ingredientinrecipe_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppinglist',
            options={'verbose_name': 'Список покупок', 'verbose_name_plural': 'Список покупок'},
        ),
    ]