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
from django.conf import settings
from bicycleparking.models import Event, SurveyAnswer, Approval

class LocationData (object):
  """Encapsulates methods for accessing the closest street or avenue
  using reverse geocoding with the Google Maps API."""

  GEOCODE_BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

  def __init__ (self, latitude, longitude) :
     """Defines the local variables: only latitude and longitude are parameters."""
     self.latitude = latitude
     self.longitude = longitude
     self.closest = self.requestLocation ()

  def update (self, data) :
     """Updates the location data: provided for compatability with the
     serializer routines."""
     self.latitude = data.get('latitude', self.latitude)
     self.longitude = data.get('longitude', self.longitude)
     self.closest = self.requestLocation ()
     
  def isValid (self) :
     """Determines whether or not the latitude and longitude provided refer
     to a valid location."""
     return self.closest != None
     
  def getClosest (self) :
     """Returns the closest street or avenue once the LocationData object has
     been initialized"""
     return self.closest

  def getLocationName (self, resp) :
     """Returns the closest street or avenue name from the reverse geocoding 
     response object from the Google Maps API."""
     result = {}
     if resp != None :
        if resp['status'] == 'OK':
           for address in resp['results']:
               for component in address['address_components']:
                  if 'route' in component['types']:
                     result['location'] = component['long_name']
               if result:
                  break
     return result
    
  def requestLocation (self) :
      """Makes a request to the Google Maps API with the selected latitude and longitude to return a reverse geocode response."""
      payload = {
         'latlng': "%s,%s" % (self.latitude, self.longitude),
         'key': settings.MAPS_API_KEY
      }
      resp = requests.get(self.GEOCODE_BASE_URL + '?', params=payload)
      return self.getLocationName(resp.json())
