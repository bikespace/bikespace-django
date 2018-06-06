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
from bicycleparking.models import Area
from bicycleparking.models import Intersection2d
from bicycleparking.models import SurveyAnswer
from bicycleparking.intersection import Intersection

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

  def __init__ (self, answer, ipAddress) :
     """Initializes the class with the following fields:
        errors: (array) the list of exception objects raised 
        when: (timestamp) the time the object was constructed
        fromWhere: (string) the originating Internet address
        survey: (SurveyAnswer class) data input by the caller
        area: (Area class) the area the request was made in
        loc (raw sql record) location of the closest intersection"""

     self.errors = []
     self.when = utils.timezone.now ()
     self.fromWhere = ipAddress
     self.survey = answer     
     self.loc = LocationData (self.survey.latitude, self.survey.longitude)
     if self.loc.isValid () :
        self.area = self.loc.getArea ()
     else :
        self.area = None

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

  def getIP (self) :
     """Gets the the internet protocol address associated with the request."""
     return self.fromWhere

  def getClosest (self) :
     """Gets the intersection closest to the location."""
     if self.isValid () :
        return Intersection (self.loc.getLocationCode ())
     else :
        return None

  def getMajor (self) :
     """Gets the major intersection closest to the location."""
     result = None
     if self.isValid () and self.area == None :
        result = Intersection (self.loc.getMajor ().gid)
     elif self.isValid () :
        result = Intersection (self.area.major)
     return result

  def getDistance (self) :
     """Gets the approximate distance from the supplied coordinates to the 
     intersection in meters"""
     if self.loc != None :
        return self.loc.getDistance ()
     else:
        return None

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
     tmp = ("\t\tfrom: {ip}\n\t\tintersection: {gid}\n\t\tcoord: ({lat}, {lng})\n",
            "\t\tdistance: {dist}\n\t\ttime: {t}\n")
     if self.isValid () :
        closest = self.loc.getLocationCode ();
     else : 
        closest = 'undefined'

     print (tmp[0].format (ip = self.fromWhere, gid = closest, 
                           lat = self.survey.latitude, lng = self.survey.longitude))
     print (tmp[1].format (dist = self.getDistance (), t = self.getTime ()))
     if len (self.errors) > 0 :
         print ("\t*** errors detected ***")
         for e in self.errors :
            print (e)
         print ("\t********")


  def output (self) :
     """Copies the current geocode and temporal data out to the database,
     using django database management facilities. Adds a pin record if one
     does not exist for the closest intersection."""

     if self.isValid () and self.area == None:
        self.area = self.loc.makeArea ()

     if self.area != None :
        inserted = Event (sourceIP = self.fromWhere, area = self.area, 
                          distance = self.loc.getDistance (), timeOf = self.when, 
                          answer = self.survey)
        inserted.save ()
        return True
     else :
        return False
