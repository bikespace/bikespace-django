# MIT License
# Copyright 2017,Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Civic Tech Toronto, Cycle Toronto, Code 4 Canada, and the 
# City of Toronto
#
# Record selector for a test subset. Tis program reads the coordinates
# from a test database and selects the closest entries to those coordinates, 
# which allows the selection of a test subset of the intersections large enough 
# for meaningful testing but small enough to permit the efficient construction
# of a database for testing the geocode functions. 
#
# Modified 
# Purpose 
#
import psycopg2
import sys
import xml.etree.ElementTree as ET

DB_HOST="127.0.0.1"
DB_USER="postgres"
DB_PW=""

def create_subset (cursor, fileId) :
  """Reads the definition of a set of locations and constructs a subset of 
  area specifications according to the following rules: the subset consists
  of a deduped set of locations near the selected (longitude/latitude)
  location. The subset ofmajor locations consists of the five closest 
  major intersections, and the subset of closest intersections consists of
  the ten closest intersections."""
 
  print ("\t\tconstructing test table subset from {0}".format (fileId, output))
  
  entries = readGeoEntries (fileId)
  cursor.execute ("CREATE TABLE test_subset (LIKE intersection2d);")

  for test in entries :
     header = "\tprocessing place name: {name: <40}\tlat/long: {latitude}:{longitude}"
     print (header.format (**test))
     select_test_data (test, cursor)     
 
def readGeoEntries (fn) :
  """Parses the xml input and extracts the list of elements defining the 
     places to test and generate test data"""
  result = []
  doc = ET.parse (fn)
  list = doc.getroot ()
  for place in list :
     if place.tag == "place" :
        result.append (processPlace (place))
  return result

def processPlace (place) :
  """Processes the selected location data from the xml element definition."""
  struc = {}
  for part in place :
     struc [part.tag] = part.text
  return struc

def select_test_data (location, cursor) :
  """Selects the closest 10 intersections and the closest 5 major
     intersections and copies them into a temporary table to create
     a limited (and unduplicated) test data set. This makes it possible 
     to create and run tests using files of manageable size."""
  majorSubsetSQL = """INSERT INTO test_subset
                         SELECT gid, int_id, intersec5, classifi6, classifi7, 
                               longitude, latitude, objectid, geom
                            FROM intersection2d
                            ORDER BY geom <-> st_setsrid(st_makepoint(%(longitude)s,%(latitude)s),4326) 
                            LIMIT 5
                         ON CONFLICT DO NOTHING;"""
  closestSubsetSQL = """INSERT INTO test_subset
                           SELECT gid, int_id, intersec5, classifi6, classifi7, 
                                  longitude, latitude, objectid, geom
                              FROM intersection2d
                              ORDER BY geom <-> st_setsrid(st_makepoint(%(longitude)s,%(latitude)s),4326)
                              LIMIT 10
                           ON CONFLICT DO NOTHING;"""

  cursor.execute (majorSubsetSQL, location)     
  cursor.execute (closestSubsetSQL, location)     
  
try:
  connection = psycopg2.connect ("dbname='intersection' host='{0}' user = '{1}' password = '{2}'".format (DB_HOST, DB_USER, DB_PW))
  cursor = connection.cursor ()
  create_subset (cursor, "coords.xml")
  connection.commit ()
except psycopg2.Warning as warning:
  if warning.pgerror != None: 
     print (warning.pgerror)
  else:
     try :
        et = errorcodes.lookup(warning.pgcode)
        print (et)
     except KeyError as secondaryError:
        print ("unknown warning in postgres link")
except psycopg2.Error as error:
  if error.pgerror != None: 
     print (error.pgerror)
  else:
     try :
        et = errorcodes.lookup(warning.pgcode)
        print (et)
     except KeyError as secondaryError:
        print ("unknown error in postgres link")

