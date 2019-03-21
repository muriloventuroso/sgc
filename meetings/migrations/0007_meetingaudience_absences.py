# Generated by Django 2.0.7 on 2019-03-20 19:06

from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('congregations', '0006_auto_20190320_1423'),
        ('meetings', '0006_remove_meetingaudience_absences'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingaudience',
            name='absences',
            field=djongo.models.fields.ArrayReferenceField(blank=True, default=[], on_delete=djongo.models.fields.ArrayReferenceField._on_delete, to='congregations.Publisher', verbose_name='Absences'),
            preserve_default=False,
        ),
    ]