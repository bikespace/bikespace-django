# MIT License
# Copyright 2017,Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Civic Tech Toronto, Cycle Toronto, Code 4 Canada, and the 
# City of Toronto
#
# Created 2017
# Purpose define serializers for endpoints
#
# Modified 2018 05 30 
# Purpose add location endpoint serializer
# 

from rest_framework import serializers
from django.contrib.postgres.fields import JSONField
from bicycleparking.models import SurveyAnswer
from bicycleparking.models import Picture
from bicycleparking.models import BetaComments

class SurveyAnswerSerializer (serializers.ModelSerializer) :

    class Meta:
        model = SurveyAnswer
        fields = ('latitude', 'longitude', 'survey')

class BetaCommentSerializer (serializers.ModelSerializer) :
    
    class Meta:
        model = BetaComments
        fields = ("comment",)

class LocationDataSerializer (serializers.Serializer) :
  """Serializes data to the Location object."""
  
  latitude = serializers.FloatField (min_value = 43.58149, max_value = 43.886692)
  longitude = serializers.FloatField (min_value = -79.61179, max_value = -79.114705)

  def create(self, validated_data):
     return Comment (validated_data ['latitude'], validated_data ['longitude'])

  def update(self, instance, validated_data):
     instance.update (validated_data)
     return instance  
