from rest_framework import serializers
from django.contrib.postgres.fields import JSONField
from bicycleparking.models import SurveyAnswer
from bicycleparking.models import Picture

class SurveyAnswerSerializer (serializers.ModelSerializer) :

    class Meta:
        model = SurveyAnswer
        fields = ('latitude', 'longitude', 'survey')

class BetaCommentSerializer (serializers.ModelSerializer) :
    
    class Meta:
        model = SurveyAnswer
        fields = ('latitude', 'longitude', 'survey')
