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
# Modified 2018 07 12
# Purpose add dashboard endpoint
#
# Modified 2019 02 21
# Purpose require authentication for moderation and redirect unauthenticated 
#         users attempting to access the moderation page to the login page
#
# Modified
# Purpose
#

from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
import json
import base64
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import FileResponse
from django.core.files.base import ContentFile
from django.contrib import admin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from datetime import datetime

from rest_framework import generics
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
import os.path
import os

from rest_framework.response import Response
from rest_framework import status

from bicycleparking.serializers import SurveyAnswerSerializer
from bicycleparking.serializers import BetaCommentSerializer
from bicycleparking.models import SurveyAnswer
from bicycleparking.models import Picture
from bicycleparking.models import BetaComments
from bicycleparking.models import Approval
from bicycleparking.models import Event
from bicycleparking.uploader import Uploader
from bicycleparking.geocode import Geocode
from bicycleparking.LocationData import LocationData
from bicycleparking.CollectedData import CollectedData
from bicycleparking.Moderate import Moderate

# Create your views here.

def index(request):
    return render(request, 'bicycleparking/index.html', {})

class SurveyAnswerList(generics.ListCreateAPIView):
    """Generates the main table entries from the user's survey input, generates
    the geographical aggregation data (closest and closest major intersection), 
    and accesses the survey data to obtain the URI for a picture submitted and
    stored separately."""
    queryset = SurveyAnswer.objects.all()
    serializer_class = SurveyAnswerSerializer
    authentication_classes = ()
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
        """Takes a set of POST parameters containing the limits of the 
        map viewport and returns a JSON string containing the details
        of all the approved pins in the selected rectangle.
        
        The data returned by this call will depend on the settings in 
        the CollectedData object, but they will generally include the
        names of the closest and the closest major intersection, the
        time of the request and the span of time requested for parking, 
        the problem as defined by the user and a URI describing the 
        picture (if any) associated with the request."""
        
        data = request.body.decode ('utf-8')
        if data :
           param = json.loads (data)
        else :
           param = {}
        return self.access (param)

    def access (self, param) :
        """Provides access to the database for both POST and GET requests."""
        # print(param)
        upLeft = lowRight = None
        if 'upper_left' in param :
            upLeft = param ['upper_left']
        if 'lower_right' in param :
            lowRight = param ['lower_right']
        data = CollectedData (upLeft, lowRight)
        result = { 'dashboard' : data.get () }
        return JsonResponse (result)

class LocationNameRequest (APIView) :
    """Wraps the location name object for retrieving data from the LocationData
    object."""
    authentication_classes = ()
    
    def post (self, request) :
        """Takes a set of GET or POST parameters containing the lat/long and returns a JSON
        string containing the names of the closest and the closest major intersection;
        note, if the closest intersection is a major intersection, these fields will 
        contain the same value."""
        data = request.data
        if data :
           param = data
        else :
           param = {}
        # print(param)
        data = LocationData (param ['latitude'], param ['longitude'])
        return JsonResponse (data.getIntersectionNames ())
              
class DownloadPicture(APIView):
    uploader = Uploader()

    def get(self, request, filename, format=None):
        ipAddress = request.META['REMOTE_ADDR']

        print ('getting picture from {}'.format (ipAddress))
        if ipAddress != "127.0.0.1" and filename:
            try:
               ctype = "image/" + os.path.splitext(filename)[1]
               return HttpResponse(self.uploader.fromS3 (filename), content_type=ctype)
            except:
                return HttpResponse(status=500)
        elif ipAddress == "127.0.0.1" :
            try :
               return FileResponse(open('test/pic/' + filename, 'rb'))
            except :
               return HttpResponse (status=500)
        else :
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

class ModerationRequest (APIView):
    """Implements the moderation AJAX handler, with the login requirement (the
    originating program must provide a valid login cookie with the request). 
    Adds the identifier of the authenticated user to the moderation request
    to allow the system to track the moderators who make changes."""
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        """Handles an AJAX request from the moderation page, extracting
        the data passed as a body of the AJAX request and adding the name
        of the originating user before instantiating a moderation database
        access controller and passing the request into it."""
        # print(request.data)
        # print (request.user.username)
        data = request.data
        data ['moderator'] = request.user.username
        content = {}
        if 'status' in data and 'event' in data :
            # print(data)
            mod = Moderate ()
            mod.approve (data)
            content = {'id': data ['event'], 'state':'success'}
        else:
            content={'id':None,'state':'error'}
        return Response(content)

class submissions_to_moderate (APIView):
    """Handles the user request, passed as an http get, to list reports in
    need of moderation."""
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
       """Handles a get request; if the request does not come from an 
       authenticated user, redirect to a login page.""" 
       context = {}
       
       if not request.user.is_authenticated() :
          #print("User not authenticated")
          return HttpResponseRedirect ('login')
       approved_event_ids = Approval.objects.values_list('approved')  # already approved events
       unapproved_events = Event.objects.exclude(id__in=approved_event_ids)  # only show unapproved events

       context ['unapproved_events'] = Moderate ().getUnmoderated ()
       context ['moderator'] = request.user.username
       #print ("CONTEXT",context)

       return render(request, 'bicycleparking/moderation.html', context)
