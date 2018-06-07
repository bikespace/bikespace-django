# MIT License
# Copyright 2017,Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Civic Tech Toronto, Cycle Toronto, Code 4 Canada, and the 
# City of Toronto
#
# Modified 2018 05 29 
# Purpose derived from Geocode for separate access to location data           
# 

import requests
import datetime
import django.utils as utils
from bicycleparking.models import Event
from bicycleparking.models import Area
from bicycleparking.models import Intersection2d
from bicycleparking.models import SurveyAnswer
from bicycleparking.intersection import Intersection

class LocationData (object):
  """Encapsulates methods for accessing the geographical databases and 
  determining the closest of some type of intersection: any or major."""

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

  def __init__ (self, latitude, longitude) :
     """Defines the local variables: only latitude and longitude are parameters."""
     self.latitude = latitude
     self.longitude = longitude
     self.closest = self.getIntersectionData ()
     self.errors = []

  def update (self, data) :
     """Updates the location data: provided for compatability with the
     serializer routines."""
     self.latitude = data.get('latitude', self.latitude)
     self.longitude = data.get('longitude', self.longitude)
     self.closest = self.getIntersectionData ()
     
  def isValid (self) :
     """Determines whether or not the latitde and longitude provided refer
     to a valid location, and whether or not the intersection lookup found
     valid intersection data."""
     return self.closest != None

  def getIntersectionNames (self) :
     """Derive a map with the names of the closest major and minor
     intersections."""
     self.getIntersectionData ()
     result = {}
     if self.closest != None :
        result ['closest']  = self.closest.intersec5 
        result ['major'] = self.getMajor ().intersec5
     return result

  def getDistance (self) :
     """Gets the approximate distance from the supplied coordinates to the 
     intersection in meters"""
     if self.closest != None :
        return self.closest.distance * 1.11E+5
     else:
        return None

  def getLocationCode (self) :
     """Returns the location code for the current intersection."""
     
     if self.isValid () :
        return self.closest.gid
     else : 
        return None  

  def getArea (self) :
     """Reads Area database record that goes with the intersection closest to the
     selected point, and returns it. If the database does not yet contain such a 
     record, returns None."""
     result = None
     if self.isValid () and Area.objects.filter (closest = self.closest.gid) :
        result = Area.objects.get (closest = self.closest.gid)
     return result 

  def makeArea (self) :
     """Creates and returns the area definition object. Calling this method will
     create a row in the Area table in the database."""
     return Area.objects.create (closest = self.closest.gid, 
                                 major = self.getMajor ().gid)

  def getIntersectionData (self) :
     """Prepares the request to the geocode database of intersections;
     if the database contains the supplied latitude and longitude, look
     up the nearest intersection and the nearest minor intersection,
     and store both in the object. This method filters the latitude 
     and longitude data submitted to a bounding box. If the latitude 
     does not fall in this box, the method sets the geographic data to 
     empty, which the test in isValid will reject."""

     inLat = LocationData.latLimits [0] < self.latitude < LocationData.latLimits [1]
     inLong = LocationData.longLimits [0] < self.longitude < LocationData.longLimits [1]
     result = None

     try :
        if inLat and inLong :
           result = self.lookupIntersection (LocationData.closestSQL, self.latitude, self.longitude)
     except Exception as error:
        self.errors.append (error)

     return result

  def getMajor (self) :
      """Gets and returns the location of the major intersection nearest to the
      closest intersection. This method determines whether the closest intersection 
      is itself a major intersection. Ifso, it simply returns the identifier of the
      closest intersection. If the closest intersection is not a major intersection,
      it issues a request against the geographic database to find the nearest major
      intersection to the current intersection and returns the resulting identifier. 
      This method assumes a valid location input parameter; if the caller passes in 
      an invalid location, the method will throw."""

      if self.closest.classifi6 == 'MJRSL' or self.closest.classifi6 == 'MJRML' :
         return self.closest
      else :
         return self.lookupIntersection (LocationData.majorSQL, 
                                         self.closest.latitude, self.closest.longitude)
    
  def lookupIntersection (self, sql, latt, longt) :
      """Translates the selected data into a django data database request."""

      location = {}
      location ['lat'] = float (latt)
      location ['long'] = float (longt)
      query = Intersection2d.objects.raw (sql, location)
      return query [0]
