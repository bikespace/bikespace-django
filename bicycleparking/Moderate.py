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

from bicycleparking.models import SurveyAnswer, Event, Approval, Picture, Edit

class Moderate (object):
  """Implements a moderation protocol for the pictures in the requests.""" 

  FIELD_MAP = { 'latitude' : 'latitude', 'longitude' : 'longitude', 'comment' : 'comments' }

  def getUnmoderated (self) :
     """Implements an html interface to list unmoderated requests."""
     return self.getPictures (Event.objects.filter (approval = None))

  def approveList (self, list) :
     """Calls the approve and edit function on multiple elements in the list."""   
     for request in list :
        self.approve (request)

  def approve (self, request_data) :
     """Records the moderated records in the approval table in the database, 
     together with the identifier of the user who approved the request."""
     if 'event' in request_data and 'moderator' in request_data :
        eis = request_data ['event'] 
        eventId = int (eis)
        userId = request_data ['moderator']
     else :
        raise ModerationError (request_data)

     mod_status = 'OK'
     if 'status' in request_data :
        mod_status = request_data ['status']
     event = Event.objects.get (id__exact = eventId)

     if Approval.objects.filter (id__exact = eventId).exists ():
        approval = Approval.objects.get (approved__exact = eventId)
        approval.status = mod_status
     else :
        approval = Approval (approved = event, moderatorId = userId, status = mod_status)
        
     # print (vars(approval))
     approval.save ()

     self.editValues (event.answer, request_data)

  def getPictures (self, list) :
     """Returns a list of dictionaries to apply to the django template for 
     creating the moderation list."""

     result = []
     for event in list :
        if Approval.objects.filter (id__exact = event.id).exists ():
           print ("invalid field encountered {}".format (event.id))       
        eventEntry = {}
        eventEntry ['id'] = link = event.id
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

  def editValues (self, answer, request) :
     """Loops through the allowed edit fields and modifies the data values the
     moderator is permitted to edit, recording the edits in the edit table."""

     coords = ('latitude', 'longitude')
     edited = False
     for edit in ('latitude', 'longitude', 'comment') :
        field = Moderate.FIELD_MAP [edit]

        if edit in request and self.updated (request [edit], field, answer, edit in coords):
           print ("{} updated".format (edit))
           record = Edit (by = request ['moderator'], field = edit, edited = answer)
           if edit in coords :
              setattr (answer, field, float (request [edit]))
           elif hasattr (answer, field) :
              setattr (answer, field, request [edit]) 
           elif (hasattr (answer, 'survey')) :
              answer.survey [field] = request [edit]
           edited = True
           record.save ()
     if edited :
        answer.save ()
   #      print ('\trequest edited')     # !!!
   #      for fc in ('latitude', 'longitude', 'comment') : # !!!
   #         print ("{} : {}".format (fc, getattr (answer, Moderate.FIELD_MAP [fc]))) # !!!
   #   else :                            # !!!
   #      print ('\trequest not edited') # !!!

  def updated (self, input, field, answer, isFloat) :
     """Determines whether or not the user has edited a field; used to
        determine whether to change the data and record an edit. If the 
        request contains a value not present in the answer object, the
        field is created. Otherwise the existing field is compared with
        the input; if they do not match, an update is performed."""

     if isFloat and hasattr (answer, field):
        value = getattr (answer, field)
        return float (input) != value
     elif hasattr (answer, field) :
        return input != getattr (answer, field)   
     elif hasattr (answer, 'survey') and hasattr (answer.survey, field) :
        value = getattr (answer.survey, field)    
        return input != value
     else :
        return True
      

class ModerationError (Exception):
  """Define a moderation error handler with the specific input error."""

  def __init__(self, message, request):
     """Defines the class as a subclass of Exception"""

     super().__init__(message)

     self.errorCond = []
     for missing in ('event', 'moderator') :
        self.errorCond.append ('missing ' + 'missing')
     self.status = 'OK'
     if self.status in request :
        self.status = request ['status']

