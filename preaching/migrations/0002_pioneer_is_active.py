# Generated by Django 2.0.7 on 2019-03-21 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preaching', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pioneer',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
    ]
