# Generated by Django 3.1.7 on 2021-03-26 10:27

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name'], 'verbose_name': 'Ingredient', 'verbose_name_plural': 'Ingredients'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(100, 'vegetarian'), (150, 'macrobiotic diet'), (160, 'mediterrenean diet'), (170, 'vegan diet'), (180, 'raw food'), (190, 'old recipes'), (200, 'fastfood'), (210, 'baking'), (220, 'gluten free')], max_length=35, verbose_name='Tags'),
        ),
    ]
