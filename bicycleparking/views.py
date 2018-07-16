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
# Modified 2018 06 01 
# Purpose add location endpoint
#
# Modified
# Purpose
#

import json
import base64
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.files.base import ContentFile
from datetime import datetime

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
from bicycleparking.LocationData import LocationData
from bicycleparking.CollectedData import CollectedData

# Create your views here.

def index(request):
    return render(request, 'bicycleparking/index.html', {})

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

class DashboardRequest (APIView) :
    """Wraps the location name object for retrieving data from the LocationData
    object."""
    
    def post (self, request) :
        """Takes a set of POST parameters containing the  and returns a JSON
        string containing the names of the closest and the closest major intersection;
        note, if the closest intersection is a major intersection, these fields will 
        contain the same value."""

        
        return self.access (json.loads (request.body))

    def access (self, param) :
        """Provides access to the database for both POST and GET requests."""
        # print(param)
        data = LocationData (param ['latitude'], param ['longitude'])
        return JsonResponse (data.getIntersectionNames ())
           
class LocationNameRequest (APIView) :
    """Wraps the location name object for retrieving data from the LocationData
    object."""
    
    def post (self, request) :
        """Takes a set of GET or POST parameters containing the  and returns a JSON
        string containing the names of the closest and the closest major intersection;
        note, if the closest intersection is a major intersection, these fields will 
        contain the same value."""
        param = json.loads (request.body)
        print(param)
        data = LocationData (param ['latitude'], param ['longitude'])
        return JsonResponse (data.getIntersectionNames ())
           

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
    renderer_classes = (JSONRenderer, )
    uploader = Uploader()

    def post(self, request, filename, format=None):
        file_obj = self.request.data['picture']
        ipAddress = request.META['REMOTE_ADDR']

        format, imgstr = file_obj.split(';base64,') 
        ext = format.split('/')[-1] 

        file = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        print ("upload source address = {0}".format (ipAddress))

        if ipAddress != "127.0.0.1" :
           content = {'s3_name': self.uploader.toS3(filename, file)}
        else :
            content = { 's3_name' : 'test/picture'}
        return Response(content)
