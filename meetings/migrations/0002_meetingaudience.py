# Generated by Django 2.0.7 on 2019-03-20 18:34

import congregations.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingAudience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('filled_by', models.CharField(max_length=160, verbose_name='Filled by')),
                ('absences', djongo.models.fields.ArrayModelField(model_container=congregations.models.Publisher, verbose_name='Absences')),
                ('other', models.TextField(verbose_name='Other')),
                ('count', models.IntegerField(default=0, verbose_name='Count')),
            ],
        ),
    ]