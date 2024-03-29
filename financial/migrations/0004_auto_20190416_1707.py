# Generated by Django 2.0.7 on 2019-04-16 20:07

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0003_auto_20190412_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionCategory',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('tt', models.CharField(choices=[('R', 'Receips'), ('C', 'Checking Account'), ('O', 'Other')], max_length=1, verbose_name='Transaction Type')),
            ],
            options={
                'verbose_name': 'Transaction Category',
                'verbose_name_plural': 'Transaction Categories',
            },
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tc',
            field=models.CharField(blank=True, choices=[('C', 'Congregation'), ('O', 'World Wide Work'), ('D', 'Expense')], max_length=1, verbose_name='Transaction Code'),
        ),
    ]
