# Generated by Django 2.0.7 on 2020-03-30 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0016_auto_20191210_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(blank=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='td',
            field=models.CharField(choices=[('I', 'In'), ('O', 'Out')], max_length=2, verbose_name='Transaction Direction'),
        ),
    ]
