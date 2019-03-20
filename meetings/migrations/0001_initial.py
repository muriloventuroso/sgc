# Generated by Django 2.0.7 on 2019-03-20 12:55

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import meetings.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('congregations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Designations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendant1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designations_attendant1', to='congregations.Publisher', verbose_name='Attendant 1')),
                ('attendant2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designations_attendant2', to='congregations.Publisher', verbose_name='Attendant 2')),
                ('mic_passer1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designations_mic_passer1', to='congregations.Publisher', verbose_name='Mic Passer 1')),
                ('mic_passer2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designations_mic_passer2', to='congregations.Publisher', verbose_name='Mic Passer 2')),
                ('soundman', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designations_soundman', to='congregations.Publisher', verbose_name='Soundman')),
                ('stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designations_stage', to='congregations.Publisher', verbose_name='Stage')),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Date')),
                ('type_meeting', models.CharField(choices=[('w', 'Weekend'), ('m', 'Midweek')], max_length=1, verbose_name='Type Meeting')),
                ('weekend_content', djongo.models.fields.EmbeddedModelField(blank=True, model_container=meetings.models.WeekendContent, null=True)),
                ('midweek_content', djongo.models.fields.EmbeddedModelField(blank=True, model_container=meetings.models.MidweekContent, null=True)),
                ('designations', djongo.models.fields.EmbeddedModelField(blank=True, model_container=meetings.models.Designations, null=True)),
                ('congregation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='congregations.Congregation', verbose_name='Congregation')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
