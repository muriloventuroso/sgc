# Generated by Django 2.0.7 on 2019-04-16 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0005_auto_20190416_1710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactioncategory',
            name='tt',
        ),
    ]
