# Generated by Django 2.0.7 on 2019-03-20 12:54

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Congregation',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(
                    auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=180, verbose_name='Name')),
                ('circuit', models.CharField(max_length=20, verbose_name='Circuit')),
                ('city', models.CharField(max_length=80, verbose_name='City')),
                ('state', models.CharField(max_length=2, verbose_name='State')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(
                    auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('congregation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 to='congregations.Congregation', verbose_name='Congregation')),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(
                    auto_created=True, primary_key=True, serialize=False)),
                ('full_name', models.CharField(
                    max_length=180, verbose_name='Full Name')),
                ('address', models.CharField(blank=True,
                 max_length=200, null=True, verbose_name='Address')),
                ('email', models.CharField(blank=True,
                 max_length=180, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True,
                 max_length=80, null=True, verbose_name='Phone')),
                ('cellphone', models.CharField(blank=True,
                 max_length=80, null=True, verbose_name='Cellphone')),
                ('creation_date', models.DateTimeField(
                    auto_now_add=True, verbose_name='Creation Date')),
                ('update_date', models.DateTimeField(
                    auto_now=True, verbose_name='Update Date')),
                ('baptism_date', models.DateTimeField(
                    blank=True, null=True, verbose_name='Baptism Date')),
                ('gender', models.CharField(choices=[
                 ('f', 'Female'), ('m', 'Male')], max_length=1, verbose_name='Gender')),
                ('tags', djongo.models.fields.JSONField(verbose_name=models.CharField(choices=[('ministerial_servant', 'Ministerial Servant'), ('attendant', 'Attendant'), ('soundman', 'Soundman'), (
                    'mic_passer', 'Mic Passer'), ('reader_w', 'Reader Watchtower'), ('reader_m', 'Reader Midweek'), ('prayer', 'Prayer'), ('elder', 'Elder'), ('student', 'Student'), ('stage', 'Stage')], max_length=80))),
                ('congregation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                 to='congregations.Congregation', verbose_name='Congregation')),
            ],
            options={
                'ordering': ('full_name',),
            },
        ),
    ]
