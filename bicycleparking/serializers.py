from rest_framework import serializers
from django.contrib.postgres.fields import JSONField
from bicycleparking.models import SurveyAnswer
from bicycleparking.models import Picture

class SurveyAnswerSerializer (serializers.ModelSerializer) :
    class Meta:
        model = SurveyAnswer
        fields = ('latitude', 'longitude', 'survey')
#
# class PictureSerializer (serializers.ModelSerializer) :
#     photo_uri = serializers.CharField (allow_null = True, required = False, source = 'picture')
# 
#     class Meta :
#         model = Picture
#         fields = ('photo_uri', 'answer')