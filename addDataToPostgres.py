#this function will add rows to postgres. This function is intended as a test and should be copied and pasted into production then deleted
import psycopg2
import configparser

CONFIG = configparser.ConfigParser(interpolation=None)
CONFIG.read('db.cfg')
dbset = CONFIG['DBSETTINGS']
conn = psycopg2.connect(**dbset)
conn.set_session(autocommit=True)
cur = conn.cursor()

def addPoint(ip,lat,lon,timestamp,surveyAnswers,comments,photoUri, photoDesc):
    #ip = string, lat = float, lon = float, timestamp = int, surveyAnswers = json,comments = string
    cur.execute('INSERT INTO bicycle_parking_pins_tb (ip, latitude, longitude, point_timestamp, survey_answers, comments,photo_uri,photo_desc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(ip, lat, lon, timestamp, surveyAnswers, comments, photoUri, photoDesc))
