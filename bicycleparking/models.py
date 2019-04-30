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
# Modified 2018 05 03 
# Purpose  added beta user comment table
#
# Modified 2018 08 30
# Purpose  added edit table and status to approval table; removed string functions from models
#

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.utils.html import format_html

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
    answer = models.ForeignKey (SurveyAnswer, on_delete = models.PROTECT, default = DEFAULT_LINK)

class Event(models.Model) :
    """The event table ties the request together. Request information falls into
    three broad categories: information generated from the user, either as input 
    or based on user actions; this information resides in the SurveyAnswer table,
    linked as the answer field in the Event table/class. Information from the
    second category, information derived from the transaction itself and the 
    timestamp of the request, resides in the Event table. Finally, information
    relating the request to an aggregated geographic area resides in the area table."""

    sourceIP = models.GenericIPAddressField()
    answer = models.ForeignKey (SurveyAnswer, on_delete = models.PROTECT, default = DEFAULT_LINK)
    timeOf = models.DateTimeField (auto_now_add = True)

class Approval (models.Model) :
    """The entries in this table link to events approved for display or release 
    to the general public by a moderator."""

    timeOfApproval = models.DateTimeField (auto_now_add = True)
    moderatorId = models.TextField (default = '', null = True)
    status = models.TextField (default = 'OK')
    approved = models.ForeignKey (Event, on_delete = models.PROTECT, default = DEFAULT_LINK)

class Edit (models.Model) :
    """Records the dits to the records made by a moderator or other privileged user."""
    by = models.TextField (null = False)
    timeOfApproval = models.DateTimeField (auto_now_add = True)
    field = models.TextField (null = False);
    edited = models.ForeignKey (SurveyAnswer, on_delete = models.PROTECT, default = DEFAULT_LINK)

class BetaComments (models.Model) :
    """Contain comments made by users of the beta version -- delete after beta completed."""

    comment = models.TextField (default = None, null = True)

# other database tables NOT managed by django -- not managed = false setting
# do not change managed = false unless the databases have changed completely;
# this may erase or corrupt the geographic resource tables, then the program
# will not work.