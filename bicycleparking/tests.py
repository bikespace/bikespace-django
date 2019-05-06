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
from django.db import connections
from bicycleparking.LocationData import LocationData
from bicycleparking.models import SurveyAnswer, Event, Approval, Picture
from bicycleparking.CollectedData import CollectedData
from bicycleparking.Survey import Survey

class Geocodetest (TestCase) :

  """ Tests include:
         test_record:        Tests the processes for writing data to he database and compares
                             the database entries as created with the expected entries. 

         test_selected       Tests the process of collecting data for the dashboard. This
                             process simulates and tests the moderation process.
         
         Each of these methods uses the same test data; this consists of a dataset coded
         in xml with specifications for a location, the (known) closest intersection to the
         given location, and the (known) closest major intersection. Each test method defines
         a map, consisting of an entry for the origin, closest and (closest) major. Each 
         entry in the map in turn contains a nested map, and each entry in the nested map 
         consists of a tag name and a field name. The field name refers to a tag within the 
         corresponding xml specification, and the field name must contain a string unique 
         throughout the entire map. For each test, this map converts the test location 
         definition element to a parameter list, which the test routines will then use. 
         See the ReadGeoEntries and its subsidiary methods for more details.

         The data in the test file include both inputs and the main expected
         results to test against. Test output will indicate whether or not 
         the test execution returned the expected result, and if it does not
         return successfully the test system will return diagnostic 
         information."""

  modSrc = { 'origin' : { 'latitude' : 'latitude', 'longitude' : 'longitude' },
             'closest' : { 'name' : 'name'} }

  locations = "test/locations.xml"

        
  def test_record (self) :
     """Tests the process of creating a survey answer and saving the
     answer into the database."""

     print ("\t\ttesting geocode recording")
     sources = { 'origin' : { 'name' : 'name', 'latitude' : 'latitude', 'longitude' : 'longitude' },
                 'closest' : { 'name' : 'name'} }

     Event.objects.all ().delete ()
     SurveyAnswer.objects.all ().delete ()

     entries = self.readEntries(sources)

     for test in entries :
        self.findAndWrite(self.saveAnswer(test), test)
        
  def test_selected (self) :
     """Tests the call to collect data for the dashboard.
     
     This test collectes the entries created by the test record process and dumps
     the resulting output."""

     sources = { 'origin' : { 'latitude' : 'latitude', 'longitude' : 'longitude' },
                 'closest' : { 'name' : 'name'} }

     print ("\t\ttesting selected and moderated dashboard output")
     self.success = True
     if self.database_exists () :
        self.moderate (1.1)
        dashboard = CollectedData ()
        list = dashboard.get ()

        print ('{} entries received'.format (len (list)))
        for item in list :
           print (json.dumps (item, indent=4, separators=(',', ': ')))
     else :
        print ("No geographic database found, assuming test OK")
     self.assertTrue (self.success)

  def test_unmoderated (self) :
     """Tests the ability to access unmoderated requests."""

     print ("\t\ttesting selection of unmoderated output for moderation process")
     self.success = True
     if self.database_exists () :
        self.moderate (0.6)
        
        unmoderated = Event.objects.filter (approval = None)
        for event in unmoderated :
           link = event.answer.id
           pictures = Picture.objects.filter (answer__id = link)
           print ('<div>')
           for pmod in pictures :
              print ('<img src="{}" width="80" height="100">'.format (pmod.photo_uri))
           print ("</div>")   
     else :
        print ("No geographic database found, assuming test OK")
     self.assertTrue (self.success)

  def moderate (self, accept) :
     """Simulates the moderation process.
     
     Adds references to the modertion table and elements to the picture table to 
     test the collection methods for accessing the dashboard."""

     print ('simulating moderation')

     rejected = 0
     entries = self.readGeoEntries (Geocodetest.modSrc)
        
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
     print ("Reading test source file {0}".format (Geocodetest.locations))
     result = []
     doc = ET.parse (Geocodetest.locations)
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

  def saveAnswer (self, location) :
     """Creates an answer record as a dummy, and then writes it to the database
     to support the creation of linked data items."""
     answer = self.makeAnswer (location)
     answer.save ()
     return answer

  def makeAnswer (self, location) :
     """Constructs a dummy survey answer using the information in the location 
     element of the test data."""

     surveyTest = { 'problem_type' : self.randomProblems (),
                    'map': [[float (location ["latitude"]), float (location ["longitude"])]],
                    'happening' : [ {'date': "2019-04-28T00:23:51.000Z"}, { 'time' : ['hours'] }],
                    'comments' : "test comment"
                  }

     return SurveyAnswer (latitude = float (location ["latitude"]), 
                          longitude = float (location ["longitude"]), 
                          survey = surveyTest)

  def findAndWrite (self, answer, testData) :
     """Executes the location request, finds the data, and writes a set of test results to
     the database."""
     where = self.locate (answer, testData)
     if where != None :
        where.output ()
        return where

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

  def diagnostic (self, where, errors) :
     """Prints a set of messages for diagnostic purposes if the comparison between the
     expected and returned data fails in a test run"""
     header = "\texpected location not found: \n\t\tname: {name}\n\t\tident: {gid}\n\t\tlat: {latitude}\n\t\tlong: {longitude}" 
     print (header.format (**errors))
     print ('\tfound location {0}'.format (where.getClosest ().getIdent ()))
     print ("\n\t********** geocoded data retrieved *****")
     where.display ()


  def locate (self, answer, location) :
     """Tests the location operation without writing any information to the database.
     Returns a Survey object."""
     result = None
     data = LocationData (location ['latitude'], location ['longitude'])
     survey = Survey(answer, "127.0.0.1")
     closest = data.getClosest()

     if closest:
        if self.locationCompare(location ['name'], closest):
           result = survey
        else:
           self.success = False
     else:
        self.success = False   

     return result

  def locationCompare (self, name, result) :
     """Compares the result of a lookup to the expected item as defined in the place 
     xml element in the test file."""
     self.assertEqual(result['location'], name)
     return True