from rest_framework import serializers
from django.contrib.postgres.fields import JSONField
from bicycleparking.models import SurveyAnswer

class SurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnswer
        fields = ('latitude', 'longitude', 'point_timestamp', 'survey', 'comments', 'photo_uri', 'photo_desc')
