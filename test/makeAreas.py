import psycopg2
import sys
import xml.etree.ElementTree as ET

# DB_HOST="bikespaceto.cyyycjt98n81.us-east-1.rds.amazonaws.com"
# DB_USER="geoiuser"
# DB_PW="IU328&7t5"

DB_HOST="127.0.0.1"
DB_USER="postgres"
DB_PW=""
DB_NAME = "test_autogeo"

def create_areas (cursor, fileId, output) :
  """Reads the definition of a set of locations and constructs a set of 
  area specifications according to the following rules: each area consists
  of three places: an origin and two intersection specifications, a major 
  and a minor. Each place consists of a place element containing a name,
  latitude and longitude, an element named "what" specifying the type of
  element ('origin', 'major', or 'closest')."""
 
  print ("\t\tconstructing test area files from {0}, output to {1}".format (fileId, output))
  
  entries = readGeoEntries (fileId)
  sink = open (output, 'w')
  sink.write ('<?xml version="1.0"?>\n<data>\n')

  for test in entries :
     header = "\tprocessing place name: {name: <40}\tlat/long: {latitude}:{longitude}"
     print (header.format (**test))
     make_area (test, cursor, sink)
  sink.write ("</data>")
  sink.close ()
     
 
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

def make_area (location, cursor, sink) :
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

  location ['what'] = 'origin'
  closest = locate (location, closestSQL, cursor, 'closest')
  major = locate (closest, majorSQL, cursor, 'major')
  put_area ((location, closest, major), sink)  
  
def locate (location, sql, cursor, kind) :
  """Locates an intersection using the nearest location lookup function in
     the posgresql geospatial database containing the intersection data. Takes
     a preset location specifier and a postgresql cursor linking to the database"""

  result = { 'what' : kind }  
  cursor.execute (sql, location)

  row = cursor.fetchone ()
  for item in zip (cursor.description, row):
     name = item [0] [0]
     value = item [1]
     result [name] = value
  return result
  
def put_area (elements, sink) :
  """Puts the selected elements to the output file."""
  sink.write ("\t<area>\n")
  for instance in elements :
     put_place (instance, sink)
  sink.write ("\t</area>\n")

def put_place (place, sink) :
  """Writes a single place element."""
  fieldMap = { 'longitude' : 'longitude', 'latitude' : 'latitude', 'gid' : 'gid',
               'name' : 'name', 'intersec5' : 'name', 'classifi6' : 'type', 
               'classifi7' : 'typeId', 'what' : 'what' }
  buffer = '\t\t<place>'
  for id, value in place.items () :
     if id in fieldMap :
        elementId = fieldMap [id]
        if buffer != '' :
           buffer = buffer + "<{0}>{1}</{0}>".format (elementId, value)
        else :
           buffer = '\n\t\t\t<{0}>{1}</{0}>'.format (elementId, value)
     if len (buffer) > 60 :
        sink.write (buffer)
        buffer = ''
  buffer = buffer + '\n\t\t</place>\n'
  sink.write (buffer)   

try:
  connection = psycopg2.connect ("dbname='{0}' host='{1}' user = '{2}' password = '{3}'".format (DB_NAME, DB_HOST, DB_USER, DB_PW))
  cursor = connection.cursor ()
  create_areas (cursor, "coords.xml", "areas.xml")
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

