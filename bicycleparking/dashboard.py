# MIT License
# Copyright 2017,Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Civic Tech Toronto, Cycle Toronto, Code 4 Canada, and the 
# City of Toronto
#
# Modified 
# Purpose 
#

import json
import requests
import datetime
import django.utils as utils
from bicycleparking.models import Event
from bicycleparking.models import Area
from bicycleparking.models import Intersection2d
from bicycleparking.models import SurveyAnswer
from bicycleparking.intersection import Intersection

class Dashboard :
  """Implements the protocol for responding to requests to supply information
     for the purposes of display on the dashboard. These requests include 
     provision of location data for heat maps, and provision of count and 
     selection data for charting demand by the day of the week."""
   

  def __init__ (self) :
     """Initializes the Dashboard data access object."""
     self.errors = []

  def dispatch (self, postData) :
     """Dispatches a request from the dashboard entry point to the correct 
        routine based on the supplied request field, together with the
        dict obtained by deserializing the JSON input string."""
     
     input = json.loads (postData)
     if input ["request"] == "HeatMap" :
        self.viewPort (input)

  def viewPort (self, input) :
     """Prepares to clip the contents of the database to the designated viewport.
     """
     if input ["zoom"] < 12 :
        print ("no filter")
     elif input ["zoom"] < 14 :
        limits = self.getLimits (input ["center"], 0.1)
        print (limits)
     else :
        limits = self.getLimits (input ["center"], 0.01)
        print (limits)

  def getLimits (self, center, degrees) :
         """Finds the area to select given the center location and the radius of
        the area as defined."""
     result = {}
     result ["long"] = self.betweenLoc (center ["lng"], degrees)
     result ["lat"] = self.betweenLoc (center ["lat"], degrees)
     return result

  def betweenLoc (self, midPoint, degrees) :
         """Finds the edges of an area as defined by a specific distance from the 
        given midpoint."""
     result = {}
     result ["min"] = midPoint - (degrees / 2);
     result ["max"] = midPoint + (degrees / 2);
     return result

