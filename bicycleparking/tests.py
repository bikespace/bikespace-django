# MIT License
# Copyright 2017, Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Code 4 Canada, Civic Tech Toronto, Cycle Toronto, and the 
# City of Toronto
#
# Written 2017 09 10
#
# Modified 2017 11 05
# Purpose Test intersection database lookups
#
# Modified 2017 11 12 
# Purpose add recording test
#
# Modified 2018 06 01
# Purpose add tests for LocationData object
#
# Modified 2018 06 26
# Purpose  Amplify documentation
#
# Modified 2018 07 18
# Purpose add dashboard selector test
#
# Modified 2018 07 18
# Purpose add dashboard selector test
#
# Modified 2018 07 23
# Purpose add moderation test
#

from django.test import TestCase
import psycopg2
import xml.etree.ElementTree as ET
import time
import json
import random
import django.utils as utils
from django.db import connections
from bicycleparking.LocationData import LocationData
from bicycleparking.models import SurveyAnswer, Event, Approval, Picture
from bicycleparking.CollectedData import CollectedData

class Test (TestCase) :

  """ Tests include:
         test_location:      Tests the process for requesting the nearest street or avenue
                             compares the results with the expected locations. 

         test_record:        Tests the process for writing the survey data to the database. 

         test_selected       Tests the process of collecting data for the dashboard. This
                             process simulates and tests the moderation process.

         test_unmoderated    Tests the ability to access unmoderated requests.
         
         Each of these methods uses the same test data; this consists of a dataset coded
         in xml with specifications for a location and the (known) closest street or avenue to the
         given location. Each test method defines a map, consisting of an entry for the origin
         and closest. Each entry in the map in turn contains a nested map, and each entry in the
         nested map consists of a tag name and a field name. The field name refers to a tag within the 
         corresponding xml specification, and the field name must contain a string unique 
         throughout the entire map. For each test, this map converts the test location 
         definition element to a parameter list, which the test routines will then use. 
         See the ReadEntries and its subsidiary methods for more details.

         The data in the test file include both inputs and the main expected
         results to test against. Test output will indicate whether or not 
         the test execution returned the expected result."""

  locations = "test/locations.xml"

  def test_location(self):
     """Tests the process of requesting the nearest street or avenue and
     compares the results with the expected locations
     """

     print ("\t\ttesting location request")
     sources = { 'origin' : {'latitude' : 'latitude', 'longitude' : 'longitude' },
                 'closest' : { 'name' : 'name'} }

     entries = self.readEntries(sources)

     for test in entries :
        self.locateAndCompare (test)
        
  def test_record (self) :
     """Tests the process of making a survey answer from the test data and
     saving the survey answer into the database."""

     print ("\t\ttesting survey recording")
     sources = { 'origin' : { 'latitude' : 'latitude', 'longitude' : 'longitude' },
                 'closest' : { 'name' : 'name'} }

     Event.objects.all ().delete ()
     SurveyAnswer.objects.all ().delete ()

     entries = self.readEntries(sources)

     for test in entries :
        self.saveAnswer(test)
        
  def test_selected (self) :
     """Tests the call to collect data for the dashboard.
     
     This test collects the entries created by the test record process and dumps
     the resulting output."""

     sources = { 'origin' : { 'latitude' : 'latitude', 'longitude' : 'longitude' },
                 'closest' : { 'name' : 'name'} }

     print ("\t\ttesting selected and moderated dashboard output")
     self.success = True

     self.moderate (1.1)
     dashboard = CollectedData ([44.0, -80.0], [43.0, -79.0])
     list = dashboard.get ()

     print ('{} entries received'.format (len (list)))
     for item in list :
        print (json.dumps (item, indent=4, separators=(',', ': ')))

     self.assertTrue (self.success)

  def test_unmoderated (self) :
     """Tests the ability to access unmoderated requests."""

     print ("\t\ttesting selection of unmoderated output for moderation process")
     self.success = True
     self.moderate (0.6)
        
     unmoderated = Event.objects.filter (approval = None)
     for event in unmoderated :
        link = event.answer.id
        pictures = Picture.objects.filter (answer__id = link)
        print ('<div>')
        for pmod in pictures :
           print ('<img src="{}" width="80" height="100">'.format (pmod.photo_uri))
        print ("</div>")
        
     self.assertTrue (self.success)

  def moderate (self, accept) :
     """Simulates the moderation process.
     
     Adds references to the modertion table and elements to the picture table to 
     test the collection methods for accessing the dashboard."""

     sources = { 'origin' : { 'latitude' : 'latitude', 'longitude' : 'longitude' },
             'closest' : { 'name' : 'name'} }

     print ('simulating moderation')

     rejected = 0
     entries = self.readEntries (sources)
        
     for test in entries :
        answer = self.saveAnswer (test)
        uri = 'http://park_pic_{}.jpg'.format (answer.id)
        pic = Picture (photo_uri = uri,  answer = answer)
        pic.save ()

     eventSet = Event.objects.all () 
     for event in eventSet :
        if (random.random () < accept) :
           approval = Approval (approved = event, moderatorId = "testJGS")
           approval.save ()
        else :
           rejected = rejected + 1

     if rejected > 0 :
        print ('rejected count: {}'.format (rejected))

  def readEntries (self, sources) :
     """Reads data to test the search and database management routines."""
     print ("Reading test source file {0}".format (Test.locations))
     result = []
     doc = ET.parse (Test.locations)
     root = doc.getroot ()
     for element in root :
        if element.tag == "location" :
           result.append (self.processLocation (element, sources))
     return result

  def processLocation (self, element, sources) :
     """Processes an location element in the XML description, assigning fields 
     according to the name mappings contained in the sources dictionary."""
     result = { }
     for nested in element :
        if nested.tag == 'place':
           result.update (self.selectElements (self.processPlace (nested), sources))
     return result

  def selectElements (self, elements, toSelect) :
     """Constructs a dictionary of items as selected from the input
     elements and mapped to the appropriate names."""
     result = { }
     if 'what' in elements :
        tagMap = toSelect [elements ['what']]
        for name, value in elements.items () :
           if name in tagMap :
              result [tagMap [name]] = value
     return result    

  def processPlace (self, place) :
     """Processes the entry descrbing a place in the xml file."""
     struc = {}
     for part in place :
        struc [part.tag] = part.text
     return struc

  def locateAndCompare (self, location) :
     """Tests the location operation without writing any information to the database."""
     data = LocationData (location ['latitude'], location ['longitude'])
     closest = data.getClosest()

     if not closest:
        self.success = False

     self.locationCompare (location ['name'], closest ['location'])

  def locationCompare (self, expected, result) :
     """Compares the result of a lookup to the expected item as defined in the place 
     xml element in the test file."""
     self.assertEqual(expected, result)

  def saveAnswer (self, location) :
     """Creates an answer record as a dummy, and then writes it to the database
     to support the creation of linked data items."""
     answer = self.makeAnswer (location)
     answer.save ()
     inserted = Event (sourceIP = "127.0.0.1", timeOf = utils.timezone.now (), 
                           answer = answer)
     inserted.save ()  
     return answer

  def makeAnswer (self, location) :
     """Constructs a dummy survey answer using the information in the location 
     element of the test data."""

     surveyTest = { 'problem_type' : self.randomProblems (),
                    'map': [[float (location ["latitude"]), float (location ["longitude"])]],
                    'happening' : [ {'date': "2019-04-28T00:23:51.000Z"}, { 'time' : ['hours'] }],
                    'comments' : "test comment",
                    'location' : location['name']
                  }

     return SurveyAnswer (latitude = float (location ["latitude"]), 
                          longitude = float (location ["longitude"]), 
                          survey = surveyTest)

  def randomProblems (self) :
     """Return a randomized list of possible problems."""

     poss = ['absent', 'full', 'damaged', 'abandoned', 'other']

     result = []
     for item in poss :
        if random.random () < 0.2 :
            result.append (item)
     if (len (result) == 0) :
        result = [ random.choice (poss) ]
     return result