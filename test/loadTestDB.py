# MIT License
# Copyright 2017,Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Civic Tech Toronto, Cycle Toronto, Code 4 Canada, and the 
# City of Toronto
#
# Constructor for a test database. Constructs a standard request recording 
# database to test programs and functions designed to access records from
# the request recording data. This permits programmers to test functions against
# a standard set of request records, which will return a set of expected 
# results to compare with the actual test output.
#
# Modified 2018 11 29
# Purpose  generate json fields in survey table
#
import psycopg2
import sys
import random
import xml.etree.ElementTree as ET
import json

DB_HOST="127.0.0.1"
DB_USER="postgres"
DB_PW=""
SOURCE_DB = "intersection"
SINK_DB = "bike_parking_toronto"

def flushTestDB (db) :
  """Erases all of the entries in the test tables."""
  
  cursor = db.cursor ()
  tables = [ 'approval', 'area', 'event', 'picture', 'surveyanswer' ]

  for t in tables :
     cmd = 'delete from bicycleparking_{};'.format (t)
     print (cmd);
     cursor.execute (cmd);
  
  db.commit ()
  cursor.close

def construct (cursor, fileId, sink) :
  """Reads the definition of a set of transactions and inserts the 
     corresponding records into the test database."""
 
  print ("\t\tconstructing test database from {0}".format (fileId))
  
  entries = readTransactions (fileId)

  for test in entries :
     header = "\tprocessing place name: {name: <40}\tlat/long: {latitude}:{longitude}"
     print (header.format (**test))
     recordTransaction (test, cursor, sink)
     
 
def readTransactions (fn) :
  """Parses the xml input and extracts the list of elements defining the 
     test transactions."""
  result = []
  doc = ET.parse (fn)
  list = doc.getroot ()
  for transaction in list :
     if transaction.tag == "transaction" :
        result.append (processTransaction (transaction))
  return result

def processTransaction (transaction) :
  """Processes the selected transaction data from the xml element definition."""
  struc = {}
  for field in transaction :
     struc [field.tag] = field.text
  return struc

def recordTransaction (transaction, cursor, sink) :
  """Creates an area specifier containing three 'place' elements describing the selected
  location, the major and the closest intersections, and writes it out as an area element to
  the result file."""
  majorSQL = """SELECT gid, int_id, intersec5, classifi6, classifi7, 
                       longitude, latitude, objectid, geom,
                       geom <-> st_setsrid(st_makepoint(%(longitude)s,%(latitude)s),4326) as distance
                FROM intersection2d
                WHERE classifi6 = 'MJRSL' or classifi6 = 'MJRML'
                ORDER BY distance
                LIMIT 1;"""
  closestSQL = """SELECT gid, int_id, intersec5, classifi6, classifi7, 
                         longitude, latitude, objectid, geom,
                         geom <-> st_setsrid(st_makepoint(%(longitude)s,%(latitude)s),4326) as distance
                  FROM intersection2d
                  ORDER BY distance 
                  LIMIT 1;"""

  areas = {}
  areas ['closest'] = locate (transaction, closestSQL, cursor)
  areas ['major'] = locate (areas ['closest'], majorSQL, cursor)

  transaction ['ip'] = '127.0.0.1'
  transaction ['area'] = put_area (areas, sink)
  transaction ['answer'] = put_survey_answer (transaction, sink)
  transaction ['distance'] = areas ['closest']['distance']
  
  put_event (transaction, sink)
  
def locate (transaction, sql, cursor) :
  """Locates an intersection using the nearest location lookup function in
     the posgresql geospatial database containing the intersection data. Takes
     a preset location specifier and a postgresql cursor linking to the database"""

  result = { }  
  cursor.execute (sql, transaction)

  row = cursor.fetchone ()
  for item in zip (cursor.description, row):
     name = item [0] [0]
     value = item [1]
     result [name] = value
  return result
  
def put_area (elements, sink) :
  """Puts the selected areas to the database."""
  template = """insert into bicycleparking_area (closest, major) values 
                (%(closest)s, %(major)s) returning id;"""
  links = {}
  links ['closest'] = elements ['closest'] ['gid']
  links ['major'] = elements ['major'] ['gid']
  sink.execute (template, links)
  return sink.fetchone () [0]

def makeSurveyJson (transaction) :
  """Generates a problem description matching the survey definition in the
     working database."""

  durations = ["overnight","overnight+", "days", "4-8hours", "minutes", ">1hour", 
               "hours", "1-2hours"]
  problem_types = [ 'full', 'absent', 'damaged', 'badly', 'unusable', 'other']

  result = {}
  result ['map'] = [ [ float (transaction ['latitude']), float (transaction ['longitude']) ] ]
  result ['happening'] = [ { 'date' : transaction ['time'], 
                              'time' : random.choice (durations) } ]
  result ['problem_type'] = [ random.choice (problem_types) ]

  print (result)
  return json.dumps (result)

def put_survey_answer (transaction, sink) :
  """Puts the survey location data into the database."""
  template = """insert into bicycleparking_surveyanswer 
                (latitude, longitude, survey, comments) values
                (%(latitude)s, %(longitude)s, %(survey)s, %(comments)s) 
                returning id;""" 
  transaction ['survey'] = makeSurveyJson (transaction)
  transaction ['comments'] = 'this is a test'
  sink.execute (template, transaction)
  return sink.fetchone () [0]

def put_event (transaction, sink) :
  """Puts the dummy event record."""
  template = """insert into bicycleparking_event ("sourceIP", "timeOf", distance, 
                                                  answer_id, area_id) values
                                                  (%(ip)s, %(time)s, %(distance)s, 
                                                  %(answer)s, %(area)s);"""
  sink.execute (template, transaction)
  print (transaction)

try:
  resource = psycopg2.connect ("dbname='{0}' host='{1}' user = '{2}' password = '{3}' port=5435".format (SOURCE_DB, DB_HOST, DB_USER, DB_PW))
  source = resource.cursor ()
  to = psycopg2.connect ("dbname='{0}' host='{1}' user = '{2}' password = '{3}' port=5435".format (SINK_DB, DB_HOST, DB_USER, DB_PW))
  sink = to.cursor ()
  construct (source, "transactions.xml", sink)
  to.commit ()
  source.close ()
  sink.close ()
  resource.close ()
  to.close ()
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

