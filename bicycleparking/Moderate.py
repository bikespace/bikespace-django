# MIT License
# Copyright 2017, Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Code 4 Canada, Civic Tech Toronto, Cycle Toronto, and the 
# City of Toronto
#
# Written 2018 07 23
#
# Modified 2018 08 30
# Purpose getUnmoderated returns a dictionary with moderation values
#
# Modified 
# Purpose
#

from bicycleparking.models import SurveyAnswer, Event, Area, Intersection2d, Approval, Picture

class Moderate (object):
  """Implements a moderation protocol for the pictures in the requests.""" 

  def getUnmoderated (self) :
     """Implements an html interface to list unmoderated requests."""
     return self.getPictures (Event.objects.filter (approval = None))

  def approveList (self, list) :
     """Calls the approve and edit function on multiple elements in the list."""   
     for request in list :
        self.approve (request)

  def approve (self, response) :
    """Records the moderated records in the approval table in the database, 
    together with the identifier of the user who approved the request."""
    if 'event' in response and 'moderator' in response :
       eventId = response ['event']
       userId = response ['moderator']
    else :
       raise ModerationError (response)

    mod_status = 'OK'
    if 'status' in response :
       mod_status = response ['status']
    
    event = Event.object.get (id = eventId)
    approval = Approval (approved = event, moderatorId = userId, status = mod_status)
    approval.save ()
    self.editValues (event.answer, response)

  def getPictures (self, list) :
     """Returns a list of dictionaries to apply to the django template for 
     creating the moderation list."""

     result = []
     for event in list :
        eventEntry = {}
        eventEntry ['id'] = link = event.answer.id
        eventEntry ['time'] = event.timeOf
        eventEntry ['comments'] = event.answer.comments
        eventEntry ['location'] = self.where (event.answer)
        eventEntry ['problem'] = event.answer.survey ['problem_type']
        eventEntry ['pictures'] = self.pic (Picture.objects.filter (answer__id = link))
        result.append (eventEntry)
     
     return result

  def where (self, answer) :
    """Gets the location of the pin from the value provided by the caller. 
    Normally this will be the pin location contained in the latitude and 
    longitude fields of the survey answer."""    
    result = {}
    result ['longitude'] = answer.longitude
    result ['latitude'] = answer.latitude 
    return result   

  def pic (self, list) :
     """Gets the list of pictures uploaded by the user."""   
     result = []
     for pmod in list :
        result.append (pmod.photo_uri)
     return result

  def makeCondition (self, source) :
     """Makes a condition value based on the response provided by the 
     moderation process."""
     condition = 'OK'
     if 'status' in response :
        if condition in ('OK', 'rejected', 'deferred') :
           condition = response ['status'];
        else :
           raise moderationError ('error in status', source)
     return condition 

  def editValues (self, answerId, request) :
     """Loops through the allowed edit fields and modifies the data values the
     moderator is permitted to edit, recording the edits in the edit table."""

     coords = ('latitude', 'longitude')
     edited = False
     toEdit = Answer.object.get (id = answerId)
     for edit in ('latitude', 'longitude', 'comment') :
        if edit in request : 
           record = Edit (by = request ['moderator'], field = edit, edited = toEdit)
           if edit in coords :
              setattr (toEdit, edit, float (request [edit]))
           else :
              setattr (toEdit, edit, request [edit])
           edited = True
     if edited :
        toEdit.save ()
      

class ModerationError (Exception):
  """Define a moderation error handler with the specific input error."""

  def __init__(self, message, request):
     """Defines the class as a subclass of Exception"""

     super().__init__(message)

     self.errorCond = []
     for missing in ('event', 'moderator') :
        self.errorCond.append ('missing ' + 'missing')
     self.status = 'OK'
     if status in request :
        self.status = request ['status']

