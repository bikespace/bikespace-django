from django.db import models

# Create your models here.
class SurveyAnswer(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    ip = models.IntegerField()
    point_timestamp = models.DateTimeField()
    #survey = models.JSONField()
    comments = models.TextField(default=None)
    photo_uri = models.TextField(default=None)
    photo_desc = models.TextField(default=None)
