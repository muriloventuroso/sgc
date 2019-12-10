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
    duration_treasure = models.CharField(max_length=20, verbose_name=_("Duration"), null=True, blank=True)
    reading = models.BooleanField(default=False, verbose_name=_("Reading"))
    room_treasure = models.CharField(
        max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], default="A", verbose_name=_("Room"))

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
    duration_apply = models.CharField(max_length=20, verbose_name=_("Duration"), null=True, blank=True)
    room_apply = models.CharField(
        max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], default="A", verbose_name=_("Room"))

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
    duration_living = models.CharField(max_length=20, verbose_name=_("Duration"), null=True, blank=True)

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
    attendants = models.ArrayReferenceField(
        to=Publisher, verbose_name=_("Attendants"), on_delete=models.SET_NULL, null=True, blank=True,
        related_name="designations_attendants")
    mic_passers = models.ArrayReferenceField(
        to=Publisher, verbose_name=_("Mic Passers"), on_delete=models.SET_NULL, null=True, blank=True,
        related_name="designations_mic_passers")


class Meeting(models.Model):
    _id = models.ObjectIdField()
    date = models.DateField(verbose_name=_("Date"))
    type_meeting = models.CharField(
        max_length=1, verbose_name=_("Type Meeting"), choices=[('w', _("Weekend")), ('m', _("Midweek"))])
    congregation = models.ForeignKey(Congregation, verbose_name=_("Congregation"), on_delete=models.CASCADE)
    weekend_content = models.EmbeddedModelField(model_container=WeekendContent, null=True, blank=True)
    midweek_content = models.EmbeddedModelField(model_container=MidweekContent, null=True, blank=True)
    designations = models.EmbeddedModelField(model_container=Designations, blank=True)
    objects = models.DjongoManager()

    class Meta:
        ordering = ['date', ]
        verbose_name = _("Meeting")
        verbose_name_plural = _("Meetings")


class MeetingAudience(models.Model):
    _id = models.ObjectIdField()
    date = models.DateField(verbose_name=_("Date"))
    filled_by = models.CharField(max_length=160, verbose_name=_("Filled by"))
    absences = models.ArrayReferenceField(to=Publisher, verbose_name=_("Absences"), blank=True)
    other = models.TextField(verbose_name=_("Other"), blank=True)
    count = models.IntegerField(verbose_name=_("Count"), default=0)
    congregation = models.ForeignKey(Congregation, verbose_name=_("Congregation"), on_delete=models.CASCADE)
    objects = models.DjongoManager()

    class Meta:
        ordering = ['date', ]
        verbose_name = _("Meeting Audience")
        verbose_name_plural = _("Meetings Audience")


class SpeakerOut(models.Model):
    _id = models.ObjectIdField()
    date = models.DateField(verbose_name=_("Date"))
    theme = models.CharField(max_length=200, verbose_name=_("Theme"), null=True, blank=True)
    speaker = models.ForeignKey(
        Publisher, verbose_name=_("Speaker"), null=True, blank=True, on_delete=models.SET_NULL)
    congregation_dest = models.CharField(
        max_length=200, verbose_name=_("Congregation Destination"), null=True, blank=True)
    congregation = models.ForeignKey(Congregation, verbose_name=_("Congregation"), on_delete=models.CASCADE)
    objects = models.DjongoManager()

    class Meta:
        ordering = ['date', ]
        verbose_name = _("Speaker Out")
        verbose_name_plural = _("Speakers Out")


class Speech(models.Model):
    _id = models.ObjectIdField()
    theme = models.CharField(max_length=200, verbose_name=_("Theme"))
    number = models.IntegerField(verbose_name=_("Number"))
    last_update = models.CharField(verbose_name=_("Last Update"), max_length=20)
    objects = models.DjongoManager()

    def __str__(self):
        return '{} - {} {}'.format(self.number, self.theme, self.last_update)


class CountSpeech(models.Model):
    _id = models.ObjectIdField()
    speech = models.ForeignKey(Speech, verbose_name=_("Speech"), on_delete=models.CASCADE)
    congregation = models.ForeignKey(Congregation, verbose_name=_("Congregation"), on_delete=models.CASCADE)
    dates = models.ListField(default=[], verbose_name=_("Dates"))
    objects = models.DjongoManager()
