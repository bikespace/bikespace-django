# MIT License
# Copyright 2017,Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Civic Tech Toronto, Cycle Toronto, Code 4 Canada, and the 
# City of Toronto
#
# Created 2018 05 29 
# Purpose derived from Geocode for separate access to location data           
# 
# Modified
# Purpose 
# 

import requests
import datetime
import django.utils as utils
from bicycleparking.models import Event, SurveyAnswer, Approval

class LocationData (object):
  """Encapsulates methods for accessing the geographical databases and 
  determining the closest of some type of intersection: any or major."""

  GEOCODE_BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
  MAPS_API_KEY = 'AIzaSyA73LhqHU5DzT-G7azXj6UAZ-z3MD8TmLY'
  latLimits = (-90, 90)
  longLimits = (-180, 180)

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
     
     
  def getClosest (self) :
      return self.closest

  def getIntersectionNames (self) :
     """Derive a map with the names of the closest major and minor
     intersections."""
     result = {}
     if self.closest != None :
        if self.closest['status'] == 'OK':
           for address in self.closest['results']:
               for component in address['address_components']:
                  if 'route' in component['types']:
                     result['major'] = component['long_name']
               if result:
                  break
     return result

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
           result = self.lookupIntersection (self.latitude, self.longitude)
     except Exception as error:
        self.errors.append (error)

     return result
    
  def lookupIntersection (self, lat, lng) :
      """Translates the selected latitude and longitude into a Google Maps API reverse geocode response."""
      payload = {
         'latlng': "%s,%s" % (lat, lng),
         'key': self.MAPS_API_KEY
      }
      resp = requests.get(self.GEOCODE_BASE_URL + '?', params=payload)
      return resp.json()
