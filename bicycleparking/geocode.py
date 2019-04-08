# MIT License
# Copyright 2017,Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Civic Tech Toronto, Cycle Toronto, Code 4 Canada, and the 
# City of Toronto
#
# Modified 2017 10 17 
# Purpose access to remote postal codes service replaced by call to
#         intersection database           
# 
# Modified 2017 11 04 
# Purpose Pin table renamed to Area table
#                    
# Modified 2017 11 05 
# Purpose Change definition of closest major intersection from the major 
#         closest to request location to the major intersection closest 
#         to the closest intersection  
#
# Modified 2018 05 30
# Purpose Separate out the location access calculations from the overall
#         database management, to permit requests for nearest locations
#         to be processed.
#

import requests
import datetime
import django.utils as utils
from bicycleparking.LocationData import LocationData
from bicycleparking.models import Event
from bicycleparking.models import SurveyAnswer

class Geocode :
  """Defines a geographic coding object with seven immutable attributes:
  the latitude and longitude of the location to specify, the closest
  intersection as defined in the City of Toronto centerline intersection
  table, the closest major intersection, the source internet address, 
  the time of the request, and the survey answer associated with the 
  request together with any comments and optionally a picture. This
  class includes an output routine to generate an event entry and 
  relate it to a pin in the pin table and the survey answer in the 
  survey table."""

  ##  public (published) methods

  def __init__ (self, answer) :
     """Initializes the class with the following fields:
        errors: (array) the list of exception objects raised 
        when: (timestamp) the time the object was constructed
        fromWhere: (string) the originating Internet address
        survey: (SurveyAnswer class) data input by the caller
        area: (Area class) the area the request was made in
        loc (raw sql record) location of the closest intersection"""

     self.errors = []
     self.when = utils.timezone.now ()
     self.survey = answer     
     self.loc = LocationData (self.survey.latitude, self.survey.longitude)

  def isValid (self) :
     """Determines whether or not the latitde and longitude provided refer
     to a valid location, and whether or not the intersection lookup found
     valid intersection data."""
     if self.loc != None :
        return self.loc.isValid ()
     else :
        return False

  def getTime (self) :
     """Gets the date and time the caller submitted the request."""
     return self.when

  def displayErrors (self) :
     """If the error detection routines detected any errors in execution,
        display the diagnostic output from all errors and return a 'True'
        value. If the error list contains no entries, return 'False'."""
     if len (self.errors) > 0 :
        self.display ()
        return True
     else :
        return False

  def display (self) :
     """Displays the current status on the output as a formatted report
     for testing purposes."""
     tmp = ("\t\tcoord: ({lat}, {lng})\n", "\t\ttime: {t}\n")

     print (tmp[0].format (lat = self.survey.latitude, lng = self.survey.longitude))
     print (tmp[1].format (t = self.getTime ()))

     if len (self.errors) > 0 :
         print ("\t*** errors detected ***")
         for e in self.errors :
            print (e)
         print ("\t********")


  def output (self) :
     """Copies the current geocode and temporal data out to the database,
     using django database management facilities. Adds a pin record if one
     does not exist for the closest intersection."""

     if self.survey != None :
        inserted = Event (timeOf = self.when, answer = self.survey)
        inserted.save()
        return True
     else :
        return False
