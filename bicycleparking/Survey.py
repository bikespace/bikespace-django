# MIT License
# Copyright 2017,Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Civic Tech Toronto, Cycle Toronto, Code 4 Canada, and the 
# City of Toronto
#
# Created 2019 05 06 
# Purpose derived in place of removed Geocode class         
# 
# Modified
# Purpose 
# 

import requests
import datetime
import django.utils as utils
from django.conf import settings
from bicycleparking.models import Event, SurveyAnswer, Approval

class Survey (object):
  """Defines a survey object used to save the survey answer to the database."""

  def __init__ (self, answer, ipAddress) :
     """Defines the local variables: survey is the survey answer, when is the 
    time the object was constructed, and fromWhere is the originating IP address."""
     self.survey = answer
     self.when = utils.timezone.now ()
     self.fromWhere = ipAddress
     
  def isValid (self) :
     """Determines whether or not the survey answer is valid."""
     return self.survey.survey != None

  def output (self) :
      """Copies the survey answer and temporal data to the database using 
      django database management facilities."""

      if self.isValid() :
         inserted = Event (sourceIP = self.fromWhere, timeOf = self.when, 
                           answer = self.survey)
         inserted.save ()
         return True
      else :
         return False