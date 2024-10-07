# Generated by Django 5.1.1 on 2024-10-07 10:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='initial_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(999999999999.99)]),
        ),
    ]
