from django.db import models

# Create your models here.
class SurveyAnswer(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    ip = models.IntegerField()
    timestamp = models.DateTimeField()
    #survey = models.JSONField()
    comment = models.TextField()