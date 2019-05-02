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
from bicycleparking.geocode import Geocode
from bicycleparking.LocationData import LocationData
from bicycleparking.models import SurveyAnswer, Event, Approval, Picture
from bicycleparking.CollectedData import CollectedData

class Geocodetest (TestCase) :

  """ Tests include:
         test_location:      tests a series of geocode values read from an xml test data file,
                             accessing the intersection database published by the City of
                             Toronto to locate the entries in the test data and compare the 
                             intersection data lookups with expected results.

         test_names_lookup:  Tests the LocationData object lookup methods and the methods to
                             return the intersection identifiers as strings for display.

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

  modSrc = { 'origin' : { 'name' : 'name', 'latitude' : 'latitude', 'longitude' : 'longitude' }, 
             'closest' : {}, 'major' : {} } 
  areas = "test/areas.xml"   
    
    
  def test_location (self) :
     """Tests the location requests without writing data to the database."""

     sources = { 'origin' : { 'name' : 'name', 'latitude' : 'latitude', 'longitude' : 'longitude' }, 
                 'closest' : { 'gid' : 'gid' }, 'major' : { } }

     self.load_geo_test_subset ();
     print ("\t\ttesting geocode location")
     self.success = True
     if self.database_exists () :
        entries = self.readGeoEntries (sources)

        for test in entries :
           self.locate (self.makeAnswer (test), test)
     else :
        print ("No geographic database found, assuming test OK")
     self.assertTrue (self.success)

  def test_names_lookup (self) :
     """Tests the names lookup method by accessing the lookup and 
     comparing the names with the string defined in the text element entry."""

     sources = { 'origin' : { 'name' : 'name', 'latitude' : 'latitude', 'longitude' : 'longitude' }, 
                 'closest' : { 'gid' : 'gid', 'name' : 'closestname'}, 
                 'major' : { 'name' : 'majorname', 'gid' : 'major_gid' } }

     print ("\t\ttesting geocode location")
     self.success = True
     if self.database_exists () :
         self.nameLookup (sources)
     else :
         print ("No geographic database found, assuming test OK")
     self.assertTrue (self.success)
        
  def test_record (self) :
     """Tests the process of accessing the geographic database and then 
     writing the information received and synthesized into the database."""

     # self.load_geo_test_subset ();
     print ("\t\ttesting geocode recording")
     self.success = True
     sources = { 'origin' : { 'name' : 'name', 'latitude' : 'latitude', 'longitude' : 'longitude' }, 
                 'closest' : { 'gid' : 'gid' }, 'major' : { 'gid' : 'major_gid' } }

     if self.database_exists () :
        Event.objects.all ().delete ()
        Area.objects.all ().delete ()
        SurveyAnswer.objects.all ().delete ()
        entries = self.readGeoEntries (sources)
        
        for test in entries :
           self.findAndWrite (self.saveAnswer (test), test)

        for entry in entries :
           self.verifyArea (entry)
        self.assertTrue (self.success)
        
  def test_selected (self) :
     """Tests the call to collect data for the dashboard.
     
     This test collectes the entries created by the test record process and dumps
     the resulting output."""

     sources = { 'origin' : { 'latitude' : 'latitude', 'longitude' : 'longitude' }, 
                 'closest' : { 'name' : 'closestname'}, 'major' : { 'name' : 'majorname' } }

     print ("\t\ttesting selected and moderated dashboard output")
     self.success = True
     if self.database_exists () :
        entries = self.readGeoEntries (sources)
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

  def nameLookup (self, sources) :
     """Tests the main names lookup functions: these lokup a given location, find the
     closest intersection and the closest major, and return both names. The endpoint
     that calls this method then packages the output in a JSON string and returns it 
     to the caller."""
     entries = self.readGeoEntries (sources)
       
     for test in entries :
        success = True
        location = LocationData (float (test ['latitude']), float (test ['longitude']))
        result = location.getIntersectionNames ()

        if (result ['closest'] == test ['closestname']) :
           print ('OK: {0}'.format (result ['closest']))
        else :
           success = False
           print ('error: {0} <> {1}'.format (result ['closest'], test ['closestname'])) 

        if result ['major'] == test ['majorname'] :
           print ('OK: {0}'.format (result ['closest']))
        else :
           success = False
           print ('error: {0} <> {1}'.format (result ['closest'], test ['closestname'])) 

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
        code = Geocode (answer, '192.168.1.225')
        code.output ()

     eventSet = Event.objects.all () 
     for event in eventSet :
        if (random.random () < accept) :
           approval = Approval (approved = event, moderatorId = "testJGS")
           approval.save ()
        else :
           rejected = rejected + 1

     if rejected > 0 :
        print ('rejected count: {}'.format (rejected))  
        
  def load_geo_test_subset (self) :
     """Once the django test routines have created the test databases, load the 
        geospatial (gis) reference database with the subset of the intersections
        and/or other elements the tests require."""

     try :
        self.makeGeoDB (connections ['geospatial'])
        self.loadGeoData (connections ['geospatial'], "test/test_data.sql")
     except Exception as error :
        print (error)

  def makeGeoDB (self, connection):
     """Executes the required commands to convert an existing Postgresql 
        database into a GIS enabled database with a GIS schema."""

     make_GIS_db = ["CREATE SCHEMA postgis;",
                    "ALTER DATABASE test_intersection SET search_path = public, postgis, contrib;",
                    "SET search_path = public, postgis, contrib;",
                    "CREATE EXTENSION postgis SCHEMA postgis;", "SELECT postgis_full_version();"]

     try :
        cursor = connection.cursor ()
        for cmd in make_GIS_db :
           print ("executing command {0}".format (cmd))
           cursor.execute (cmd)
           if cursor.rowcount > 0 :
              print (cursor.fetchone ())
           connection.commit ()
     except psycopg2.Warning as warning :
        if warning.pgerror != None :
           print (warning.pgerror)
        else :
           print ("unknown warning in postgres link")
     except psycopg2.Error as error :
        if error.pgerror != None :
           print (error.pgerror)
        else :
           print ("unknown error in postgres link")

  def loadGeoData (self, connection, fn) :
     """Opens the selected input test file and reads it command 
        by command, executing each command using a cursor generated
        from the submitted connection to execute each command. Then
        executes test queries of the created data to verify the status
        of the newly created records."""

     with connection.cursor () as sink :
        print ("add test geographic data")
        with open (fn) as sql :
           for cmd in sql :
              try :
                 sink.execute (cmd)
              except psycopg2.Warning as warning :
                 if warning.pgerror != None :
                    print (warning.pgerror)
                 else :
                    print ("unknown warning in postgres link")
              except psycopg2.Error as error :
                 if error.pgerror != None :
                    print (error.pgerror)
                 else :
                    print ("unknown error in postgres link")
        try :
           sel = """select * from intersection2d where gid < 10;"""   
           sink.execute (sel)
           if sink.rowcount > 0 :
              print ("printing {0} rows".format (sink.rowcount))
              for p in sink.fetchall () :
                 print (p)
           else :
              print ("no rows selected")
           sink.execute ("select count (int_id) from intersection2d;")
           print (sink.fetchone ())
        except psycopg2.Warning as warning :
           if warning.pgerror != None :
              print (warning.pgerror)
           else :
              print ("unknown warning in postgres link")
        except psycopg2.Error as error :
           if error.pgerror != None :
              print (error.pgerror)
           else :
              print ("unknown error in postgres link")

  def readGeoEntries (self, sources) :
     """Reads data to test the search and database management routines."""
     print ("Reading test source file {0}".format (Geocodetest.areas))
     result = []
     doc = ET.parse (Geocodetest.areas)
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
        self.success = False
     else : 
        self.diagnostic (where, location)
        self.success = False
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
           self.success = False
     else :
        print ("\terror: {0} not found with target {1}".format (testData ['name'], int (testData ['gid']))) 
        self.success = False

  def geoCompare (self, key, where) :
     """Compares the result of a lookup to the expected item as defined in the place 
     xml element in the test file."""
     try :
        return where.getClosest ().getIdent () == key
     except Exception as error :
        self.success = False
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
        sql = 'select gid from intersection2d limit 10;'
        list = Intersection2d.objects.raw (sql)
        for i in list :
           count = count + 1 
        return count > 5
     except Exception as error :
        print (error)
        return False