from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class SurveyAnswer(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    ip = models.IntegerField()
    point_timestamp = models.DateTimeField()
    survey = JSONField(default=None)
    comments = models.TextField(default=None)
    photo_uri = models.TextField(default=None)
    photo_desc = models.TextField(default=None)
