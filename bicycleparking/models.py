from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class SurveyAnswer(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    ip = models.GenericIPAddressField()
    point_timestamp = models.DateTimeField(auto_now_add=True)
    survey = JSONField(default=dict)
    comments = models.TextField(default=None, null=True)
    photo_uri = models.TextField(default=None, null=True)
    photo_desc = models.TextField(default=None, null=True)
