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
# Modified 
# Purpose 
#
import psycopg2
import sys
import random
import xml.etree.ElementTree as ET
import json
import os

DB_HOST = os.getenv('BIKE_DB_HOST', "127.0.0.1")
DB_USER = os.getenv('BIKE_DB_USER', "postgres")
DB_PW = os.getenv('BIKE_DB_PW', 'postgres')
DB = os.getenv('BIKE_DB_NAME', "bike_parking_toronto")

def flushTestDB (db) :
  """Erases all of the entries in the test tables."""
  
  cursor = db.cursor ()
  tables = [ 'approval', 'event', 'picture', 'surveyanswer' ]

  for t in tables :
     cmd = 'delete from bicycleparking_{};'.format (t)
     print (cmd)
     cursor.execute (cmd)
  
  db.commit ()
  cursor.close

def construct (fileId, sink) :
  """Reads the definition of a set of transactions and inserts the 
     corresponding records into the test database."""
 
  print ("\t\tconstructing test database from {0}".format (fileId))
  
  entries = readTransactions (fileId)

  pictureList = os.listdir ('test/pic')
  for test in entries :
     header = "\tprocessing place name: {name: <40}\tlat/long: {latitude}:{longitude}"
     print (header.format (**test))

  for test in entries : 
     test ['picture'] = random.choice (pictureList)
     recordTransaction (test, sink)    
 
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

def recordTransaction (transaction, sink) :
  """Creates an area specifier containing three 'place' elements describing the selected
  location, the major and the closest intersections, and writes it out as an area element to
  the result file. This method writes an entry to four tables: area, survey_answer, event
  and picture."""

  transaction ['ip'] = '127.0.0.1'
  transaction ['answer'] = put_survey_answer (transaction, sink)

  put_picture (transaction, sink)  
  put_event (transaction, sink)

def put_survey_answer (transaction, sink) :
  """Puts the survey location data into the database."""
  template = """insert into bicycleparking_surveyanswer 
                (latitude, longitude, survey) values
                (%(latitude)s, %(longitude)s, %(survey)s) 
                returning id;""" 
  transaction ['survey'] = makeSurveyJson (transaction)
  sink.execute (template, transaction)
  return sink.fetchone () [0]

def makeSurveyJson (transaction) :
  """Generates a problem description matching the survey definition in the
     working database."""

  durations = ["overnight","overnight+", "days", "4-8hours", "minutes", ">1hour", 
               "hours", "1-2hours"]
  problem_types = [ 'full', 'absent', 'damaged', 'badly', 'unusable', 'other']

  result = {}
  result ['map'] = [ [ float (transaction ['latitude']), float (transaction ['longitude']) ] ]
  result ['happening'] = [ { 'date' : transaction ['time'], 'time' : random.choice (durations) } ]
  result ['problem_type'] = [ random.choice (problem_types) ]
  result ['comments'] = "test comment"

  print (result)
  return json.dumps (result)

def put_picture (transaction, sink) :
  """Puts the picture entry for the event."""
  template = """insert into bicycleparking_picture (photo_uri, answer_id) values
                                                  (%(picture)s, %(answer)s);"""
  sink.execute (template, transaction)

def put_event (transaction, sink) :
  """Puts the dummy event record."""
  template = """insert into bicycleparking_event ("sourceIP", "timeOf",
                                                  answer_id) values
                                                  (%(ip)s, %(time)s, %(answer)s);"""
  sink.execute (template, transaction)
  print (transaction)

try:
  db = psycopg2.connect ("dbname='{0}' host='{1}' user = '{2}' password = '{3}' port = 5435".format (DB, DB_HOST, DB_USER, DB_PW))
  
  flushTestDB (db)
  sink = db.cursor ()
  construct ("test/transactions.xml", sink)
  db.commit ()
  sink.close ()
  db.close ()
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

