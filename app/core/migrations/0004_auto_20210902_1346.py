# Generated by Django 2.1.15 on 2021-09-02 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_recipe'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientForARecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Ingredient')),
                ('Recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='core.IngredientForARecipe', to='core.Ingredient'),
        ),
    ]
