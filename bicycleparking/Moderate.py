# MIT License
# Copyright 2017, Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Code 4 Canada, Civic Tech Toronto, Cycle Toronto, and the 
# City of Toronto
#
# Written 2018 07 23
#
# Modified 
# Purpose
#

from bicycleparking.models import SurveyAnswer, Event, Area, Intersection2d, Approval, Picture

class Moderate (object):
  """Implements a moderation protocol for the pictures in the requests.""" 

  def getUnmoderated (self) :
     """Implements an html interface to list unmoderated requests."""

  def getPictures (self) :
     """Returns a string representing the html links to display pictures and 
     prompt for form list."""

     formText = "<form>" 
     unmoderated = Event.objects.filter (approval = None)
     for event in unmoderated :
        link = event.answer.id
        pictures = Picture.objects.filter (answer__id = link)
        formText = formText + '<div>'
        for pmod in pictures :
           formText = formText + '<img src="app/pictures/{}" width="80" height="100">'.format (pmod.photo_uri)
        formText = formText + '<button onclick="approve ({})">Approve</button>'.format (event.id)
        print ("</div>")   
        
