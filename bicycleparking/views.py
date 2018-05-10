# MIT License
# Copyright 2017,Code 4 Canada
# written by and for the bicycle parking project, a joint project of
# Civic Tech Toronto, Cycle Toronto, Code 4 Canada, and the
# City of Toronto
#
# Modified 2017 10 28
# Purpose add geocode to view
#
# Modified 2018 02 27
# Purpose added code to write to separate picture table
#
# Modified 2018 05 03
# Purpose added endpoint to handle beta user comment submission
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
from bicycleparking.serializers import BetaCommentSerializer
from bicycleparking.models import SurveyAnswer
from bicycleparking.models import Picture
from bicycleparking.models import BetaComments
from bicycleparking.uploader import Uploader
from bicycleparking.geocode import Geocode

# Create your views here.

def index(request):
    return render(request, 'bicycleparking/home.html', {})


def dashboard(request):
    return render(request, 'bicycleparking/dashboard.html', {})

class SurveyAnswerList(generics.ListCreateAPIView):
    """Generates the main table entries from the user's survey input, generates
    the geographical aggregation data (closest and closest major intersection), 
    and accesses the survey data to obtain the URI for a picture submitted and
    stored separately."""
    queryset = SurveyAnswer.objects.all()
    serializer_class = SurveyAnswerSerializer

    def perform_create(self, serializer):
        """Executes the HTTP POST request by creating four objects: the survey
        answer using the serializer, the aggregate geographic data (Geocode)
        and event record using the geocode class, and the picture record."""
        answer = serializer.save()
        pic = Picture (answer = answer, photo_uri = self.request.data ['photo_uri'])
        pic.save ()
        geocode = Geocode(answer, ipAddress=self.request.META['REMOTE_ADDR'])
        geocode.output()         

class BetaCommentList(generics.ListCreateAPIView):
    """Generic comments section for the beta release of the application.
    Users can submit any comments about the application.
    """
    queryset = BetaComments.objects.all()
    serializer_class = BetaCommentSerializer

    def perform_create(self, serializer):
        """Executes the HTTP POST request by creating four objects: the survey
        answer using the serializer, the aggregate geographic data (Geocode)
        and event record using the geocode class, and the picture record."""
        serializer.save()

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
        ipAddress = request.META['REMOTE_ADDR']
        print ("upload source address = {0}".format (ipAddress))
        if ipAddress != "127.0.0.1" :
           content = {'s3_name': self.uploader.toS3(filename, file_obj)}
        else :
            content = { 's3_name' : 'test/picture'}
        return Response(content)
