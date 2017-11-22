from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import generics
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

from rest_framework.response import Response
from rest_framework import status

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

class UploadPicture(APIView):
    parser_classes = (FileUploadParser,)
    renderer_classes = (JSONRenderer, )

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        content = {'s3_name': "toto"}
        return Response(content)