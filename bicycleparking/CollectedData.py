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
from bicycleparking.models import Event, Area, SurveyAnswer, Intersection2d, Approval

class CollectedData (object):
  """Encapsulates methods for accessing the geographical databases and 
  returning request data as approved by a moderator."""

  latLimits = (43.58149, 43.886692)
  longLimits = (-79.61179, -79.114705)
  majorSQL = """SELECT intersec5 FROM intersection2d WHERE gid = %s;"""
  closestSQL = """SELECT intersec5 FROM intersection2d WHERE gid = %s;"""

  def __init__ (self, upperLeft = None, lowerRight = None) :
     """Defines the local variables: and the bounding box"""
     if (upperLeft and lowerRight) :
        self.limits = ((lowerRight [0], upperLeft [0]), (upperLeft [1], lowerRight [1]))
     elif (upperLeft) :
        self.limits = ((longLimits [1], upperLeft [0]), (upperLeft [1], latLimits [1]))
     elif (lowerRight) :
        self.limits = ((lowerRight [0], longLimits [0]), (latLimits [0], lowerRight [1]))         
     else :
        self.limits = (longLimits [::-1], latLimits)
     self.errors = []

  def get (self) :
     """Gets the list of approved items from the request database""" 

     result = []
     list = Approval.objects.approved;
     for entry in list :
         if self.bounded (entry.answer) :
           result.append (self.accessItem (entry.area, entry.survey))

  def accessItem (self, area, survey) :
      """Takes the specifications for each individual item and constructs a single
      description object."""
      
      fromSurvey = [ { 'id' : 'pic', 'path' : ['picture']},
                     { 'id' : 'duration', 'path' : ['happening', 0, 'time'] },
                     { 'id' : 'problem', path : ['problem_type']} ]
      result = {}
      survey = JSON.loads (entry.answer.survey)
      for field in fromSurvey :
          try :
              result [field ['id']] = self.fromSurvey (survey, field ['path'])
          except Exception as err:
              errors.append (err.msg)
      result ['longitude'] = entry.answer ['longitude']    
      result ['latitude'] = entry.answer ['latitude']    

  def fromSurvey (self, base, indices) :
      if len (indices) == 0 :
          return base
      else :
          current = indices [0]
          remaining = indices [1:]
          if ((type (base) is list and type (current) is int and current < len (base)) or
              (type (base) is dict and current in base)) : 
             return self.fromSurvey (base [indices [0]], indices [1:])
          else :
             return "" 
      
  def bounded (self, survey) :
      return self.limits [0][0]  < survey.longitude < self.limits [1][0] and \
             self.limits [0][1] < survey.latitude < self.limits [0][1]  
       