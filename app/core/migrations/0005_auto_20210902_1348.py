# Generated by Django 2.1.15 on 2021-09-02 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210902_1346'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientforarecipe',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'managed': False},
        ),
    ]
