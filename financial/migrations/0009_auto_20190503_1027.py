# Generated by Django 2.0.7 on 2019-05-03 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0008_auto_20190416_1721'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['date'], 'verbose_name': 'Transaction', 'verbose_name_plural': 'Transactions'},
        ),
        migrations.AddField(
            model_name='transaction',
            name='hide_from_sheet',
            field=models.BooleanField(default=False, verbose_name='Hide from Transaction Sheet'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='td',
            field=models.CharField(choices=[('I', 'In'), ('O', 'Out'), ('OI', 'Out - In')], max_length=1, verbose_name='Transaction Direction'),
        ),
    ]
