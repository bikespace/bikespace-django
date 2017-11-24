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

import requests
import datetime
from bicycleparking.models import Event
from bicycleparking.models import Area
from bicycleparking.models import CentrelineIntersectionWgs84
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

  latLimits = (43.58149, 43.886692)
  longLimits = (-79.61179, -79.114705)
  key = "*** reserved for future use"
  majorSQL = """SELECT gid, int_id, intersec5, classifi6, classifi7, 
                       longitude, latitude, objectid, geom,
                       geom <-> st_setsrid(st_makepoint(%(long)s,%(lat)s),4326) as distance
                FROM intersection2d
                WHERE classifi6 = 'MJRSL' or classifi6 = 'MJRML'
                ORDER BY distance
                LIMIT 1;"""
  closestSQL = """SELECT gid, int_id, intersec5, classifi6, classifi7, 
                         longitude, latitude, objectid, geom,
                         geom <-> st_setsrid(st_makepoint(%(long)s,%(lat)s),4326) as distance
                  FROM intersection2d
                  ORDER BY distance 
                  LIMIT 1;"""

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
     self.when = datetime.datetime.now ()
     self.fromWhere = ipAddress
     self.survey = answer
     self.area = None

     self.loc = self.getIntersectionData ()
     if self.loc != None :
        self.area = self.getArea (self.loc)

  def isValid (self) :
     """Determines whether or not the latitde and longitude provided refer
     to a valid location, and whether or not the intersection lookup found
     valid intersection data."""
     return self.loc != None

  def getTime (self) :
     """Gets the date and time the caller submitted the request."""
     return self.when

  def getIP (self) :
     """Gets the the internet protocol address associated with the request."""
     return self.fromWhere

  def getClosest (self) :
     """Gets the intersection closest to the location."""
     if self.isValid () :
        return Intersection (self.loc.gid)
     else :
        return None

  def getMajor (self) :
     """Gets the major intersection closest to the location."""
     result = None
     if self.isValid () and self.area == None :
        result = Intersection (self.getMajorId (self.loc))
     elif self.isValid () :
        result = Intersection (self.area.major)
     return result

  def getDistance (self) :
     """Gets the approximate distance from the supplied coordinates to the 
     intersection in meters"""
     distance = None
     if self.loc != None :
        distance = self.loc.distance * 1.11E+5
     return distance

  def display (self) :
     """Displays the current status on the output as a formatted report
     for testing purposes."""
     tmp = ("\t\tfrom: {ip}\n\t\tintersection: {gid}\n\t\tcoord: ({lat}, {lng})\n",
            "\t\tdistance: {dist}\n\t\ttime: {t}\n")
     if self.isValid () :
        closest = self.loc.gid;
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
        self.area = self.makeArea ()

     if self.area != None :
        inserted = Event (sourceIP = self.fromWhere, area = self.area, 
                          distance = self.loc.distance, timeOf = self.when, 
                          answer = self.survey)
        inserted.save ()
        return True
     else :
        return False   

  ##  private (unpublished) methods

  def getIntersectionData (self) :
     """Prepares the request to the geocode database of intersections;
     if the database contains the supplied latitude and longitude, look
     up the nearest intersection and the nearest minor intersection,
     and stores both in the object. This method filters the latitude 
     and longitude data submitted to a bounding box. If the latitude 
     does not fall in this box, the method sets the geographic data to 
     empty, which the test in isValid will reject."""

     dlat = self.survey.latitude
     dlong = self.survey.longitude
     inLat = Geocode.latLimits [0] < dlat < Geocode.latLimits [1]
     inLong = Geocode.longLimits [0] < dlong < Geocode.longLimits [1]
     result = None

     try :
        if inLat and inLong :
           result = self.lookupIntersection (Geocode.closestSQL, dlat, dlong)
     except Exception as error:
        self.errors.append (error)

     return result

  def getArea (self, loc) :
     """Reads Area database record that goes with the intersection closest to the
     selected point, and returns it. If the database does not yet contain such a 
     record, returns None."""
     result = None
     if loc != None and Area.objects.filter (closest = loc.gid) :
        result = Area.get (closest = loc.gid)
     return result 

  def makeArea (self) :
     """Creates and returns the area definition object. Calling this method will
     create a row in the Area table in the database."""
     return Area.objects.create (closest = self.loc.gid, 
                                 major = self.getMajorId (self.loc))

  def getMajorId (self, loc) :
      """Gets and returns the location of the major intersection nearest to the
      closest intersection. This method determines whether the closest intersection 
      is itself a major intersection. Ifso, it simply returns the identifier of the
      closest intersection. If the closest intersection is not a major intersection,
      it issues a request against the geographic database to find the nearest major
      intersection to the current intersection and returns the resulting identifier. 
      This method assumes a valid location input parameter; if the caller passes in 
      an invalid location, the method will throw."""

      if loc.classifi6 == 'MJRSL' or loc.classifi6 == 'MJRML' :
         return loc.gid
      else :
         majorLoc = self.lookupIntersection (Geocode.majorSQL, 
                                             loc.latitude, loc.longitude)
         if majorLoc != None :
            return majorLoc.gid
         else:
            return None
    
  def lookupIntersection (self, sql, latt, longt) :
      """Translates the selected data into a django data database request."""

      location = {}
      location ['lat'] = float (latt)
      location ['long'] = float (longt)
      query = CentrelineIntersectionWgs84.objects.raw (sql, location)
      return query [0]