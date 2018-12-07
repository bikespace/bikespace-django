# MIT License
# Copyright 2017,Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Civic Tech Toronto, Cycle Toronto, Code 4 Canada, and the 
# City of Toronto
#
# Created 2018 07 05
# Purpose provide (user) dashboard access to approved requests
# 
# Modified 
# Purpose 
# 

import requests
import datetime
import json
import django.utils as utils
from bicycleparking.models import Event, Area, SurveyAnswer, Intersection2d, Approval, Picture

class CollectedData (object):
  """Encapsulates methods for accessing the geographical databases and 
  returning request data as approved by a moderator."""

  latLimits = (43.58149, 43.886692)
  longLimits = (-79.61179, -79.114705)
  sqlStmt = """SELECT * FROM intersection2d WHERE gid = %(code)s;"""

  def __init__ (self, upperLeft = None, lowerRight = None) :
     """Defines the local variables: and the bounding box"""
     if (upperLeft and lowerRight) :
        self.limits = ((upperLeft [0], lowerRight [0]), (lowerRight [1], upperLeft [1]))
     elif (upperLeft) :
        self.limits = ((upperLeft [0], CollectedData.longLimits [1]), 
                       (CollectedData.latLimits [0]), upperLeft [1])
     elif (lowerRight) :
        self.limits = ((CollectedData.longLimits [0], lowerRight [0]), 
                       (lowerRight [1], CollectedData.latLimits [1]))         
     else :
        self.limits = (CollectedData.longLimits, CollectedData.latLimits)
     self.errors = []

  def get (self) :
     """Gets the list of approved items from the request database""" 

     result = []
     list = Approval.objects.filter (status__exact = 'OK');

     for entry in list :
         if self.bounded (entry.approved.answer) :
           result.append (self.accessItem (entry.approved))
     return result

  def accessItem (self, event) :
      """Takes the specifications for each individual item and constructs a single
      description object."""

      answer = event.answer

      fromSurvey = [ { 'id' : 'duration', 'path' : ['happening', 0, 'time'] },
                     { 'id' : 'problem', "path" : ['problem_type']} ]

      result = self.getNames (event.area)
      survey = answer.survey
      for field in fromSurvey :
          try :
              key = field ['id']
              result [key] = self.fromSurvey (survey, field ['path'])
          except Exception as err:
              errors.append (err.msg)
                     
      result ['pic'] = self.getPicture (answer.id)
      result ['longitude'] = answer.longitude    
      result ['latitude'] = answer.latitude
      result ['comments'] = answer.comments
      result ['time'] = str(event.timeOf)
      result ['id'] = event.id
      return result

  def fromSurvey (self, base, indices) :
      """Gets the item in the survey by recursively scanning the index list until
      the list is empty. If the index is invalid for the type of object in the
      structure, returns empty string."""
      if len (indices) == 0 :
          return base
      else :
          current = indices [0]
          remaining = indices [1:]
          if ((type (base) is list and type (current) is int and current < len (base)) or
              (type (base) is dict and current in base)) : 
             return self.fromSurvey (base [current], remaining)
          else :
             return "" 
      
  def bounded (self, survey) :
      """Determines whether or not a pin falls within the boundaries associated
      with the request."""

      return self.limits [0][0] < survey.longitude < self.limits [0][1] and \
             self.limits [1][0] < survey.latitude < self.limits [1][1]  

  def getNames (self, area) :
     """Gets the names associated with the area supplied."""

     instr = [ { 'id' : 'majorIntersection', 'code' : area.major },
               { 'id' : 'intersection', 'code' : area.closest }]

     result = {}

     for req in instr :
        query = Intersection2d.objects.raw (CollectedData.sqlStmt, req)
        entry = query [0]
        result [req ['id']] = entry.intersec5
     return result

  def getPicture (self, id) :
     """Gets the picture from the dedicated picture reference table """ 
     result = []
     picRef = Picture.objects.filter (answer__id = id)
     for pic in picRef :
        result.append (pic.photo_uri)
     return result
