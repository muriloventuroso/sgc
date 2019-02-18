from django.contrib import admin
from djongo import models
from django.utils.translation import ugettext_lazy as _
from congregations.models import Congregation, Publisher


class WeekendContent(models.Model):
    president = models.ForeignKey(
        Publisher, verbose_name=_("President"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="weekend_president")
    speaker = models.CharField(max_length=200, verbose_name=_("Speaker"), null=True, blank=True)
    speaker_congregation = models.CharField(
        max_length=200, verbose_name=_("Speaker Congregation"), null=True, blank=True)
    theme = models.CharField(max_length=200, verbose_name=_("Theme"), null=True, blank=True)
    reader = models.ForeignKey(
        Publisher, verbose_name=_("Reader"), on_delete=models.SET_NULL, related_name="weekend_reader",
        null=True, blank=True)

    class Meta:
        abstract = True


class TreasuresContent(models.Model):
    title_treasure = models.CharField(max_length=200, verbose_name=_("Title"), null=True, blank=True)
    person_treasure = models.ForeignKey(
        Publisher, verbose_name=_("Person"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="treasures_person")
    duration_treasure = models.CharField(max_length=2, verbose_name=_("Duration"), null=True, blank=True)
    reading = models.BooleanField(default=False, verbose_name=_("Reading"))
    room_treasure = models.CharField(
        max_length=1, choices=[('A', 'A'), ('B', 'B')], default="A", verbose_name=_("Room"))

    class Meta:
        abstract = True


class ApplyYourselfContent(models.Model):
    title_apply = models.CharField(max_length=200, verbose_name=_("Title"), null=True, blank=True)
    student = models.ForeignKey(
        Publisher, verbose_name=_("Student"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="apply_student")
    assistant = models.ForeignKey(
        Publisher, verbose_name=_("Assistant"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="apply_assistant")
    duration_apply = models.CharField(max_length=2, verbose_name=_("Duration"), null=True, blank=True)
    room_apply = models.CharField(
        max_length=1, choices=[('A', 'A'), ('B', 'B')], default="A", verbose_name=_("Room"))

    class Meta:
        abstract = True


class LivingChristiansContent(models.Model):
    title_living = models.CharField(max_length=200, verbose_name=_("Title"), null=True, blank=True)
    person_living = models.ForeignKey(
        Publisher, verbose_name=_("Person"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="living_person")
    reader = models.ForeignKey(
        Publisher, verbose_name=_("Reader"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="living_reader")
    duration_living = models.CharField(max_length=2, verbose_name=_("Duration"), null=True, blank=True)

    class Meta:
        abstract = True


class MidweekContent(models.Model):
    reading_week = models.CharField(max_length=80, verbose_name=_("Reading Week"), null=True, blank=True)
    initial_song = models.CharField(max_length=3, verbose_name=_("Initial Song"), null=True, blank=True)
    initial_prayer = models.ForeignKey(
        Publisher, verbose_name=_("Initial Prayer"), null=True, blank=True,
        on_delete=models.SET_NULL, related_name="midweek_initial_prayer")
    president = models.ForeignKey(
        Publisher, verbose_name=_("President"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="midweek_president")
    treasures = models.ArrayModelField(model_container=TreasuresContent)
    apply_yourself = models.ArrayModelField(model_container=ApplyYourselfContent)
    second_song = models.CharField(max_length=3, verbose_name=_("Second Song"), null=True, blank=True)
    living_christians = models.ArrayModelField(model_container=LivingChristiansContent)
    final_prayer = models.ForeignKey(
        Publisher, verbose_name=_("Final Prayer"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="midweek_final_prayer")
    final_song = models.CharField(max_length=3, verbose_name=_("Final Song"), null=True, blank=True)

    class Meta:
        abstract = True


class Designations(models.Model):
    soundman = models.ForeignKey(
        Publisher, verbose_name=_("Soundman"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="designations_soundman")
    stage = models.ForeignKey(
        Publisher, verbose_name=_("Stage"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="designations_stage")
    attendant1 = models.ForeignKey(
        Publisher, verbose_name=_("Attendant 1"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="designations_attendant1")
    attendant2 = models.ForeignKey(
        Publisher, verbose_name=_("Attendant 2"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="designations_attendant2")
    mic_passer1 = models.ForeignKey(
        Publisher, verbose_name=_("Mic Passer 1"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="designations_mic_passer1")
    mic_passer2 = models.ForeignKey(
        Publisher, verbose_name=_("Mic Passer 2"), null=True, blank=True, on_delete=models.SET_NULL,
        related_name="designations_mic_passer2")


class Meeting(models.Model):
    _id = models.ObjectIdField()
    date = models.DateField(verbose_name=_("Date"))
    type_meeting = models.CharField(
        max_length=1, verbose_name=_("Type Meeting"), choices=[('w', _("Weekend")), ('m', _("Midweek"))])
    congregation = models.ForeignKey(Congregation, verbose_name=_("Congregation"), on_delete=models.CASCADE)
    weekend_content = models.EmbeddedModelField(model_container=WeekendContent, null=True)
    midweek_content = models.EmbeddedModelField(model_container=MidweekContent, null=True)
    designations = models.EmbeddedModelField(model_container=Designations)
    objects = models.DjongoManager()

    class Meta:
        ordering = ['date', ]


admin.site.unregister(Meeting)
admin.site.unregister(Designations)
admin.site.unregister(MidweekContent)
admin.site.unregister(LivingChristiansContent)
admin.site.unregister(ApplyYourselfContent)
admin.site.unregister(TreasuresContent)
admin.site.unregister(WeekendContent)