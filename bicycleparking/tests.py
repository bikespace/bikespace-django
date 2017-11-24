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
# Modified 
# Purpose   
#

from django.test import TestCase
import psycopg2
import xml.etree.ElementTree as ET
import time
from bicycleparking.geocode import Geocode
from bicycleparking.models import SurveyAnswer
from bicycleparking.models import Event
from bicycleparking.models import Area
from bicycleparking.models import CentrelineIntersectionWgs84
from bicycleparking.intersection import Intersection


""" Tests include:
       test_location:  tests a series of geocode values read from an xml test data file,
                       accessing the intersection database published by the City of
                       Toronto to locate the entries in the test data and compare the 
                       intersection data lookups with expected results.
       test_record:    Tests the processes for writing data to he database and compares
                       the database entries as created with the expected entries. 

                       The data in the test file include both inputs and the main expected
                       results to test against. Test output will indicate whether or not 
                       the test execution returned the expected result, and if it does not
                       return successfully the test system will return diagnostic 
                       information."""

class Geocodetest (TestCase) :

  """ Tests include:
         test_location:  tests a series of geocode values read from an xml test data file,
                         accessing the intersection database published by the City of
                         Toronto to locate the entries in the test data and compare the 
                         intersection data lookups with expected results.
         test_record:    Tests the processes for writing data to he database and compares
                         the database entries as created with the expected entries. 

                         The data in the test file include both inputs and the main expected
                         results to test against. Test output will indicate whether or not 
                         the test execution returned the expected result, and if it does not
                         return successfully the test system will return diagnostic 
                         information."""
    
  def test_location (self) :
     """Tests the location requests without writing data to the database."""
     sources = { 'origin' : { 'name' : 'name', 'latitude' : 'latitude', 'longitude' : 'longitude' }, 
                 'closest' : { 'gid' : 'gid' }, 'major' : { } }
     print ("\t\ttesting geocode location")
     if self.database_exists () :
        entries = self.readGeoEntries ("test/areas.xml", sources)

        for test in entries :
           self.locate (self.makeAnswer (test), test)
     else :
        print ("No geographic database found, assuming test OK")

  def test_record (self) :
     """Tests the process of accessing the geographic database and then 
     writing the information received and synthesized into the database."""

     print ("\t\ttesting geocode recording")
     sources = { 'origin' : { 'name' : 'name', 'latitude' : 'latitude', 'longitude' : 'longitude' }, 
                 'closest' : { 'gid' : 'gid' }, 'major' : { 'gid' : 'major_gid' } }

     if self.database_exists () :
        Event.objects.all ().delete ()
        Area.objects.all ().delete ()
        SurveyAnswer.objects.all ().delete ()
        entries = self.readGeoEntries ("test/areas.xml", sources)
        
        for test in entries :
           self.findAndWrite (self.saveAnswer (test), test)

        for entry in entries :
           self.verifyArea (entry) 

  def readGeoEntries (self, fn, sources) :
     """Reads data to test the search and database management routines."""
     print ("Reading test source file {0}".format (fn))
     result = []
     doc = ET.parse (fn)
     root = doc.getroot ()
     for element in root :
        if element.tag == "area" :
           result.append (self.processArea (element, sources))
     return result

  def processArea (self, element, sources) :
     """Processes an area element in the XML description, assigning fields 
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

     return SurveyAnswer (latitude = float (location ["latitude"]), 
                          longitude = float (location ["longitude"]), 
                          survey = "{'test' : 'empty'}", comments = "",
                          photo_uri = "", photo_desc = "")

  def findAndWrite (self, answer, testData) :
     """Executes the location request, finds the data, and writes a set of test results to
     the database."""
     where = self.locate (answer, testData)
     if where != None :
        where.output ()

  def locate (self, answer, location) :
     """Tests the location operation without writing any information to the database."""
     result = None
     where = Geocode (answer, "127.0.0.1")

     if 'gid' in location and self.geoCompare (int (location ['gid']), where) :
        location ['dist'] = where.getDistance ()
        header = "\tfound: {name} lat: {latitude} long: {longitude} distance: {dist} meters"
        print (header.format (**location))
        result = where
     elif not 'gid' in location:
        print ("\t\texpected result not found, no verification possible")
     else : 
        self.diagnostic (where, location)
     return result

  def verifyArea (self, testData) :
     """Verifies the area in the database against the test data, and dumps the event data."""

     area_loc = Area.objects.filter (closest = int (testData ['gid']))
     if area_loc :
        tmp = '\tentry found: verifying {0} from {1} at {2}'
        areaRef = area_loc.first ()
        event_loc = Event.objects.filter (area = areaRef)
        for event in event_loc :
           print (tmp.format (testData ['name'], event.sourceIP, event.timeOf))
        if areaRef.major != int (testData ['major_gid']) :
           print ("\t\terror: mismatch {0} with test data {1}".format (areaRef.major, testData ['major_gid']))
     else :
        print ("\terror: {0} not found with target {1}".format (testData ['name'], int (testData ['gid']))) 

  def geoCompare (self, key, where) :
     """Compares the result of a lookup to the expected item as defined in the place 
     xml element in the test file."""
     try :
        return where.getClosest ().getIdent () == key
     except Exception as error :
        if where == None :
           print ('geolocation undefined for {0}'.format (key))
        else :
           where.display ()   

  def diagnostic (self, where, errors) :
     """Prints a set of messages for diagnostic purposes if the comparison between the
     expected and returned data fails in a test run"""
     header = "\texpected location not found: \n\t\tname: {name}\n\t\tident: {gid}\n\t\tlat: {latitude}\n\t\tlong: {longitude}" 
     print (header.format (**errors))
     print ('\tfound location {0}'.format (where.getClosest ().getIdent ()))
     print ("\n\t********** geocoded data retrieved *****")
     where.display ()

  def database_exists (self) :
     """Determines the validity of the centerline intersection database."""
     try :
        count = 0
        sql = 'select gid from centreline_intersection_wgs84 limit 10;'
        list = CentrelineIntersectionWgs84.objects.raw (sql)
        for i in list :
           count = count + 1 
        return count > 5
     except Exception as error :
        print (error)
        return False