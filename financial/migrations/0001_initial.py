# Generated by Django 2.0.7 on 2019-03-20 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('congregations', '0006_auto_20190320_1423'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Date')),
                ('description', models.TextField(verbose_name='Description')),
                ('tc', models.CharField(choices=[('C', 'Congregation'), ('O', 'World Wide Work'), ('D', 'Bank Account Deposit'), ('S', 'World Kingdom Hall Construction')], max_length=1, verbose_name='Transaction Code')),
                ('tt', models.CharField(choices=[('R', 'Receips'), ('C', 'Checking Account'), ('O', 'Other')], max_length=1, verbose_name='Transaction Type')),
                ('td', models.CharField(choices=[('I', 'In'), ('O', 'Out')], max_length=1, verbose_name='Transaction Direction')),
                ('note', models.TextField(verbose_name='Note')),
                ('congregation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='congregations.Congregation')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
