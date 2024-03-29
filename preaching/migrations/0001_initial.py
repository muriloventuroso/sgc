# Generated by Django 2.0.7 on 2019-03-21 20:39

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('congregations', '0006_auto_20190320_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldServiceReport',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(
                    auto_created=True, primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Date')),
                ('tags', djongo.models.fields.JSONField(verbose_name=models.CharField(choices=[
                 ('auxiliary_pioneer', 'Auxiliary Pioneer'), ('regular_pioneer', 'Regular Pioneer')], max_length=80))),
                ('hours', models.IntegerField(default=0, verbose_name='Hours')),
                ('placements', models.IntegerField(
                    default=0, verbose_name='Placements')),
                ('video', models.IntegerField(
                    default=0, verbose_name='Video Showings')),
                ('return_visits', models.IntegerField(
                    default=0, verbose_name='Return Visits')),
                ('studies', models.IntegerField(default=0, verbose_name='Studies')),
                ('note', models.TextField(verbose_name='Note')),
                ('congregation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 to='congregations.Congregation', verbose_name='Congregation')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 to='congregations.Publisher', verbose_name='Publisher')),
            ],
        ),
        migrations.CreateModel(
            name='Pioneer',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(
                    auto_created=True, primary_key=True, serialize=False)),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(
                    blank=True, null=True, verbose_name='End Date')),
                ('tp', models.CharField(choices=[
                 ('a', 'Auxiliary Pioneer'), ('r', 'Regular Pioneer')], max_length=1)),
                ('congregation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 to='congregations.Congregation', verbose_name='Congregation')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 to='congregations.Publisher', verbose_name='Publisher')),
            ],
        ),
    ]
