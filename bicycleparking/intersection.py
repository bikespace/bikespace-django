# MIT License
# Copyright 2017, Cycle Toronto
# written by and for the bicycle parking project, a joint project of 
# Civic Tech Toronto, Cycle Toronto, Code 4 Canada, and the 
# City of Toronto
#
# Written 2017 10 15
#
# Modified 
# Purpose

class Intersection :
    """Defines the characterstics of an intersection, wrapping a
    CentrelineIntersectionWgs84 tale entry to obtain the data from a
    pin. This takes the integer value stored in a Pin object for the 
    closest minor and major intersection, and accesses the data from
    the geographic data model."""

    ## public (published) interface

    def __init__ (self, ident) :
        self.id = ident
        self.buffer = None

    def getIdent (self) :
        """Gets the primary key that identifies an intersection."""
        return self.id

    def isEqual (self, other) :
        """Determines whether or not one intersection value is equal to another.
        Normally, callers will use this to determine whether or not the closest
        intersection and the closest major are the same."""
        return self.id == other.getIdent ()

    def getStreets (self) :
        """Gets a description of the intersection consisting of the cross street 
        names."""
        if self.buffer == None :
            self.buffer = self.fetch ()
        return self.buffer.intersec5

    def getType (self) :
        """Gets a string description of the intersection type (major, minor, 
        one/two level, cul de sac, etc)."""
        if self.buffer == None :
            self.buffer = self.fetch ()
        return self.buffer.classifi7

    def getLongitude (self) :
        """Gets the longitude of the intersection."""
        if self.buffer == None :
            self.buffer = self.fetch ()
        return self.buffer.longitude

    def getLatitude (self) :
        """Gets the latitude of the intersection."""
        if self.buffer == None :
            self.buffer = self.fetch ()
        return self.buffer.latitude
       
    
    ## private (unpublished) support routines

    def fetch (self) :
       return Intersection2d.get (gid=self.ident)