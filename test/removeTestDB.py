import psycopg2
import sys
import xml.etree.ElementTree as ET
import os

DB_HOST=os.getenv ('BIKE_DB_HOST', 'localhost')
DB_USER=os.getenv ('BIKE_DB_USER', 'postgres')
DB_PW=os.getenv ('BIKE_DB_PW', '')

TO_DELETE = ("test_bike_parking_toronto", "test_intersection")

for dbn in TO_DELETE :
  try:
     connection = psycopg2.connect ("dbname='intersection' host='{0}' user = '{1}' password = '{2}'".format (DB_HOST, DB_USER, DB_PW))
     connection.autocommit = True
     cursor = connection.cursor ()
     print ("deleting database {0}".format (dbn))
     cursor.execute ("drop database if exists {0};".format (dbn))
     cursor.close ()
     connection.close ()
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

