from django.db import models
from django.contrib.postgres.fields import JSONField

# Survey answer as received
class SurveyAnswer(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    ip = models.GenericIPAddressField()
    point_timestamp = models.DateTimeField(auto_now_add=True)
    survey = JSONField(default=dict)
    comments = models.TextField(default=None, null=True)
    photo_uri = models.TextField(default=None, null=True)
    photo_desc = models.TextField(default=None, null=True)

# Event description derived from the survey answer, includes
# - the receivingIP address
# - the postal code
# - the relevant time
class Event(models.Model) :
    sourceIP = models.GenericIPAddressField()
    postalCode = models.TextField (default = None, null = True)
    timeOf = models.DateTimeField (auto_now_add = True)

# Parking requests consolidated by postal code
#    contains postal code (full)
class Pin (models.Model) :
    where = models.TextField (default = None, null = True)
