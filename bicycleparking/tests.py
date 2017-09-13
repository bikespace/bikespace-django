from django.test import TestCase
import xml.etree.ElementTree as ET
import time
from bicycleparking.geocode import Geocode

""" Tests include:
       GeocodeTest:  tests a series of geocode values read from an xml test data file. 
                     The data in this file include both inputs and the main expected
                     results to test against. Output of the geocodeTest will indicate
                     whether or not the test execution returned the expected result,
                     what data the test data submitted, what the methods under test
                     returned, and what the test defined as expected."""

# Create your tests here.

class Geocodetest (TestCase) :
    def test_geocode (self) :
        print ("\t\ttesting geocode data with gecode source 001\n")
        entries = self.readGeoEntries ("test/geodata_001.xml")

        # NB: this loop contains a 10-second delay at each cycle to avoid
        # multiple rapid-fire calls to the geocoding service. Please note the
        # service is throttled with a daily limit of 500 or fewer calls per 
        # day from any given IP address, so the tests should use as few
        # items within the defined boundaries as an effective test will
        # permit.  
        for test in entries :
            self.locate (test)
            time.sleep (10)

    def readGeoEntries (self, fn) :
        result = []
        doc = ET.parse (fn)
        list = doc.getroot ()
        for place in list :
            if place.tag == "place" :
                result.append (self.processPlace (place))
        return result

    def processPlace (self, place) :
        struc = {}
        for part in place :
            struc [part.tag] = part.text
        return struc

    def locate (self, location) :
        header = "\texpecting place name: {name}\n\tpostal code {code}\n\tlat/long: {lat}:{long}"
        lat = float (location ["lat"])
        longt = float (location ["long"])
        print (header.format (**location))
        where = Geocode ("loopback", lat, longt)
        pc = where.getPostalCode ()
        if pc == location ["code"] :
            print ("test results match expected value")
        else :
            mismatch = "*** results do not match. found: {0} expected: {1} ***"
            print (mismatch.format (pc, location ["code"]))
        where.display ()