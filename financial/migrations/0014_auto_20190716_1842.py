# Generated by Django 2.0.7 on 2019-07-16 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0013_auto_20190716_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='value',
            field=models.FloatField(default=0, verbose_name='Value'),
        ),
    ]