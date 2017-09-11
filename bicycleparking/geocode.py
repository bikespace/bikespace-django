# copyright header here
# written by and for the bicycle parking project, a joint project of 
# Civic Tech Toronto, Cycle Toronto, and the City of Toronto
# 

import requests
import re
import xml.etree.ElementTree as ET
import datetime
from bicycleparking.models import Event
from bicycleparking.models import Pin

class Geocode :
    """Defines a geographic coding with four immutable attributes:
    the latitude and longitude of the location to specify, the postal
    code as determined by the reverse geocoding api invoked (geocoder.ca)
    and the neighbourhood identifier. The class verifies the postal code 
    using a class variable regex, and returns the postal code or
    generates an event entry and optionally relates it to a pin in the
    pin table."""

    filter = re.compile ("\\AM\\d[A-Z]\\d[A-Z]\\d\\Z")
    latLimits = (43.58149, 43.886692)
    longLimits = (-79.61179, -79.114705)
    key = "*** reserved for future use"

    def __init__ (self, ipAddress, dlat, dlong) :
        self.latt = dlat
        self.long = dlong
        self.when = datetime.datetime.now ()
        self.fromWhere = ipAddress
        self.accessLocationData (dlat, dlong)

    def accessLocationData (self, dlat, dlong) :
        """Prepares the request to the geocoder remote api, retrieves the 
        response, and stores it in the object. Since calls to the geocoder
        API may involve a fee, this method filters the latitude and longitude
        data submitted to a bounding box. If the latitude does not fall in
        this box, the method sets the geographic data to empty, which the
        test in isValid will reject."""
        inLat = Geocode.latLimits [0] < dlat < Geocode.latLimits [1]
        inLong = Geocode.longLimits [0] < dlong < Geocode.longLimits [1]
        if inLat and inLong :
            self.invokeGeocoder (dlat, dlong)
            return True
        else :
            self.postalCode = self.neighbourhood = ""
            return False
    
    def invokeGeocoder (self, latt, longt) :
        """Invokes the selected geocoder API. This method abstracts the call 
        to the geocoder so as to make switching between geocoding API providers
        relatively straightforward."""
        location = { "latt" : str (latt), "longt" : str (longt), 
                     "reverse" : 1, "geoit" : "XML" }
        # next 2 lines fordebugging only
        t = "\n\n\t\t*** latitude: {latt} longitude: {longt}\n\n"
        print (t.format (**location))
        geoSpec = requests.get ("http://geocoder.ca", params = location)
        self.extractGeolocation (ET.fromstring (geoSpec.text))
        

    def extractGeolocation (self, element) :
        """Scans the data retrieved from the geocoder api and extracts
        the postal code and the neighbourhood definition strings. If the 
        retrieved data does not contain these values, it sets them to
        empty strings. This method abstracts the function of parsing
        returned data to facilitate switching between geocoding API
        providers."""
        self.postalCode = self.neighbourhood = ""
        for specification in element:
            # next 2 lines fordebugging only
            tt = "\t\ttag: {0}  value: {1}"
            print (tt.format (specification.tag, specification.text))
            if specification.tag == "postal" :
                self.postalCode = specification.text
            elif specification.tag == "neighborhood" :
                self.neighbourhood = specification.text

    def isValid (self) :
        """Determines whether or not the latitde and longitude provided refer
        to a valid location. This mathod potentially provides better granularity 
        than the filter in accessLocationData."""
        return Geocode.filter.match (self.postalCode)

    def getTime (self) :
        """Gets the date and time the caller submitted the request."""
        return self.when

    def getPostalCode (self) :
        """Gets the postal code found for the location, whether or not the
        postal code is valid according to the defined postal code filter."""
        return self.postalCode

    def display (self) :
        """Displays the current status on the output as a formatted report
        for testing purposes."""
        tmp = ("\tfrom: {ip}\n\tpostal code: {pc}\n\tcoord: ({lat}, {lng})\n",
               "\tneighbourhood {nh}\n\t time: {t}\n")
        print (tmp[0].format (ip = self.fromWhere, pc = self.postalCode, 
                              lat = self.latt, lng = self.long))
        print (tmp[1].format (nh = self.neighbourhood, t = self.getTime ()))

    def output (self) :
        """Copies the current geocode and temporal data out to the database,
         using django database management facilities. Adds a pin record if one
         does not exist for the current postal code."""
        if self.isValid () :
            models.Pin.objects.get_or_create (where = self.postalCode)
            inserted = models.Event (sourceIP = self.fromWhere, postalCode = self.postalCode,
                                     timeOf = self.when)
            inserted.save ()
            return True
        else :
            return False   