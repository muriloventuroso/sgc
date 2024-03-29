# Generated by Django 2.0.7 on 2019-03-20 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('congregations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='congregations.Group', verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='publisher',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active?'),
        ),
    ]
