# Generated by Django 5.1.1 on 2024-10-15 14:27

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_icon_class_name'),
        ('wallet', '0003_alter_wallet_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='icon',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.icon'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='initial_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00')), django.core.validators.MaxValueValidator(Decimal('999999999999.99'))]),
        ),
    ]
