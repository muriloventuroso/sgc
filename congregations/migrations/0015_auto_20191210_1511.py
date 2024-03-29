# Generated by Django 2.0.7 on 2019-12-10 18:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('congregations', '0014_auto_20191210_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='congregation',
            name='n_attendants',
            field=models.IntegerField(default=2, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='Number of Attendants'),
        ),
        migrations.AlterField(
            model_name='congregation',
            name='n_mic_passers',
            field=models.IntegerField(default=2, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='Number of Mic Passers'),
        ),
    ]
