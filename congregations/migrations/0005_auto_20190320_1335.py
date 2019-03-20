# Generated by Django 2.0.7 on 2019-03-20 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('congregations', '0004_publisher_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='congregation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='congregations.Congregation', verbose_name='Congregation'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='congregations.Group', verbose_name='Group'),
        ),
    ]
