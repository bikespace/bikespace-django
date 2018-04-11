# MIT License
# Copyright 2017, Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Code 4 Canada, Civic Tech Toronto, Cycle Toronto, and the 
# City of Toronto
#
# Written 2017 07 21
#
# Modified 2017 10 18
# Purpose support for multiple databases and the geocoding lookup
#
# Modified 2017 11 05 
# Purpose rename table 'Pin' to 'Area'
#
# Modified 2017 11 24
# Purpose  Incorporate de-duped intersection table
#
# Modified 2018 02 23
# Purpose  separate picture file reference into separate table
#
# Modified 
# Purpose   
#

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

# Tables in the default database as managed by the django
# process 

# default link for undefined foreign keys
DEFAULT_LINK = 1

# Survey answer as received
class SurveyAnswer(models.Model):
    """Contains the information directly input by the user or generated by user
    actions such as taking a picture. The information in this table is linked
    and tied to the geographical area information about the request by the
    Event table/class."""

    latitude = models.FloatField()
    longitude = models.FloatField()
    survey = JSONField(default=dict)
    comments = models.TextField(default=None, null=True)

class Picture (models.Model) :  
    """Contains the definition of a photograph uploaded by the user of the 
       selected parking problem."""
    photo_uri = models.TextField(default=None, null=True)
    photo_desc = models.TextField(default=None, null=True)
    answer = models.ForeignKey (SurveyAnswer, related_name = 'photo', on_delete = models.PROTECT, default = DEFAULT_LINK)

#    class Meta :
#        unique_together = ('answer', 'photo_uri')

class Area (models.Model) :
    """Area of the parking request identified by the closest intersection and the
    closest major intersection. For the sake of consistency in defining areas, the
    closest major intersection refers to the major intersection closest to the nearest
    intersection, not to the the major intersection closest to the request point.
    In database terms, in an area definition the closest intersection acts as the
    determinant and the closest major depends on it. This also means all the requests
    in an area defined by a closest intersection will have the same closest major
    intersection."""

    closest = models.IntegerField(blank=True, null = False, default = DEFAULT_LINK)
    major = models.IntegerField (blank=True, null = False, default = DEFAULT_LINK)

class Event(models.Model) :
    """The event table ties the request together. Request information falls into
    three broad categories: information generated from the user, either as input 
    or based on user actions; this information resides in the SurveyAnswer table,
    linked as the answer field in the Event table/class. Information from the
    second category, information derived from the transaction itself, such as the
    originating IP address and the timestamp of the request, resides in the Event
    table. Finally, information relating the request to an aggregated geographic 
    area resides in the area table."""

    sourceIP = models.GenericIPAddressField()
    area = models.ForeignKey (Area, on_delete = models.PROTECT, default = DEFAULT_LINK)
    answer = models.ForeignKey (SurveyAnswer, on_delete = models.PROTECT, default = DEFAULT_LINK)
    timeOf = models.DateTimeField (auto_now_add = True)
    distance = models.BigIntegerField (blank = True, null = True)

# other database tables NOT managed by django -- not managed = false setting
# do not change managed = false unless the databases have changed completely;
# this may erase or corrupt the geographic resource tables, then the program
# will not work.

class Intersection2d (models.Model):
  """Intersection definition table
     Tables in the geospatial database as defined in the settings
     for this project are not managed by django: they are loaded
     from data supplied by the city of Toronto. The following model
     definitions are obtained from introspecting the existing database
     tables created by importing a shape file, and then eliminating
     all locations duplicating the two dimensional coordinates. The 
     application will access these values but never write to them.
     
     The SQL statement to create two dimensional table with no
     elevations and no dulicated latitude and longitude values is:
     
     create table intersection2d 
       as select distinct on (longitude, latitude)
                 gid, int_id, intersec5, classifi6, classifi7, 
                 longitude, latitude, objectid, geom
          from centreline_intersection_wgs84
          order by longitude, latitude, gid;"""

  gid = models.AutoField(primary_key=True)
  int_id = models.BigIntegerField(blank=True, null=True)
  intersec5 = models.CharField(max_length=250, blank=True, null=True)
  classifi6 = models.CharField(max_length=5, blank=True, null=True)
  classifi7 = models.CharField(max_length=80, blank=True, null=True)
  longitude = models.FloatField(blank=True, null=True)
  latitude = models.FloatField(blank=True, null=True)
  objectid = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
  # The 'geom' field contains a hex string with location data and the application will 
  # never access it directly
  geom = models.TextField(blank=True, null=True)  

  class Meta:
     managed = False
     db_table = 'intersection2d'

class CentrelineIntersectionWgs84(models.Model):
  """Intersection definition table
     Tables in the geospatial database as defined in the settings
     for this project are not managed by django: they are loaded
     from data supplied by the city of Toronto. The following model
     definitions are obtained from introspecting the existing database
     tables created by importing a shape file. The application will
     access these values but never write to them."""

  gid = models.AutoField(primary_key=True)
  int_id = models.BigIntegerField(blank=True, null=True)
  elev_id = models.BigIntegerField(blank=True, null=True)
  intersec5 = models.CharField(max_length=250, blank=True, null=True)
  classifi6 = models.CharField(max_length=5, blank=True, null=True)
  classifi7 = models.CharField(max_length=80, blank=True, null=True)
  num_elev = models.SmallIntegerField(blank=True, null=True)
  elevatio9 = models.IntegerField(blank=True, null=True)
  elevatio10 = models.CharField(max_length=80, blank=True, null=True)
  elev_level = models.SmallIntegerField(blank=True, null=True)
  elevation = models.FloatField(blank=True, null=True)
  elevatio13 = models.CharField(max_length=6, blank=True, null=True)
  height_r14 = models.FloatField(blank=True, null=True)
  height_r15 = models.CharField(max_length=6, blank=True, null=True)
  x = models.FloatField(blank=True, null=True)
  y = models.FloatField(blank=True, null=True)
  longitude = models.FloatField(blank=True, null=True)
  latitude = models.FloatField(blank=True, null=True)
  objectid = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
  # The 'geom' field contains a hex string with location data and the application will 
  # never access it directly
  geom = models.TextField(blank=True, null=True)  

  class Meta:
     managed = False
     db_table = 'centreline_intersection_wgs84'

class SpatialRefSys(models.Model):
  """Reference for the internal use of the geographic query plugins in 
     Postgresql. The application routines should never access this model; 
     it is included for completeness."""

  srid = models.IntegerField(primary_key=True)
  auth_name = models.CharField(max_length=256, blank=True, null=True)
  auth_srid = models.IntegerField(blank=True, null=True)
  srtext = models.CharField(max_length=2048, blank=True, null=True)
  proj4text = models.CharField(max_length=2048, blank=True, null=True)

  class Meta:
     managed = False
     db_table = 'spatial_ref_sys'