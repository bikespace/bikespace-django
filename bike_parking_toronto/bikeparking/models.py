from django.db import models

class SurveyAnswer(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    ip = models.IntField()
    timestamp = models.DateTimeField()
    survey = models.JSONField()
    comment = models.TextField()
