# MIT License
# Copyright 2017,Code 4 Canada
# written by and for the bicycle parking project, a joint project of
# Civic Tech Toronto, Cycle Toronto, Code 4 Canada, and the
# City of Toronto
#
# Modified 2017 10 28
# Purpose add geocode to view
#
# Modified
# Purpose
#

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
import os.path

from rest_framework.response import Response
from rest_framework import status

from bicycleparking.serializers import SurveyAnswerSerializer
from bicycleparking.models import SurveyAnswer
from bicycleparking.uploader import Uploader
from bicycleparking.geocode import Geocode

# Create your views here.


def index(request):
    return render(request, 'bicycleparking/home.html', {})


def dashboard(request):
    return render(request, 'bicycleparking/dashboard.html', {})


class SurveyAnswerList(generics.ListCreateAPIView):
    queryset = SurveyAnswer.objects.all()
    serializer_class = SurveyAnswerSerializer

    def perform_create(self, serializer):
        answer = serializer.save()
        geocode = Geocode(answer, ipAddress=self.request.META['REMOTE_ADDR'])
        geocode.output()


class DownloadPicture(APIView):
    uploader = Uploader()

    def get(self, request, filename, format=None):
        if filename:
            try:
                return HttpResponse(self.uploader.fromS3(filename), content_type="image/" + os.path.splitext(filename)[1])
            except:
                return HttpResponse(status=500)
        else:
            return HttpResponse(status=500)
        


class UploadPicture(APIView):
    parser_classes = (FileUploadParser,)
    renderer_classes = (JSONRenderer, )
    uploader = Uploader()

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        content = {'s3_name': self.uploader.toS3(filename, file_obj)}
        return Response(content)
