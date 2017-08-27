from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import generics

from bicycleparking.serializers import SurveyAnswerSerializer
from bicycleparking.models import SurveyAnswer

# Create your views here.
def index(request):
    return render(request, 'bicycleparking/landing.html', {})

class SurveyAnswerList(generics.CreateAPIView):
    queryset = SurveyAnswer.objects.all()
    serializer_class = SurveyAnswerSerializer

    def perform_create(self, serializer):
        serializer.save(ip=self.request.META['REMOTE_ADDR'])
