# MIT License
# Copyright 2017, Code 4 Canada
# written by and for the bicycle parking project, a joint project of 
# Code 4 Canada, Civic Tech Toronto, Cycle Toronto, and the 
# City of Toronto
#
# Written 2017 10 17
#
# Modified 
# Purpose   
#

"""
Defines the routers to dispatch requests for data from the models as defind
in the django project to the appropriate external databases as defined in the
DATABASE variable in the settings file.
"""

class GeoSpatialRouting :
  """Routes requests to the django database interface to the geospatial
  database in order to look up intersections from the submitted latitude
  and longitude coordinates."""

  # models supported by the geospatial database
  includedModels = set (['centrelineintersectionwgs84', 'spatialrefsys'])

  def db_for_read (self, model, **hints):
     """Selects the database to read from: if the caller accesses the
     intersections table model, the request is routed to the geospatial
     database, otherwise it is ignored."""

     result = None
     if model._meta.model_name in GeoSpatialRouting.includedModels :
         result = 'geospatial'
     return result

  def db_for_write (self, model, **hints):
     """Selects the database to write to: since the app should never
     actually write to the geospatial database this is included only
     for completeness."""

     result = None
     if model._meta.model_name in GeoSpatialRouting.includedModels :
         result = 'geospatial'
     return result

  def allow_relation(self, obj1, obj2, **hints):
     """Allow any relation if a both models refer to tables in the
     geospatial database. Ideally the program would support relations 
     between multiple databases, but django does not currently allow 
     that, so the router only allows relations handled by django for
     the default database"""

     result = False
     if not (obj1._meta.model_name in GeoSpatialRouting.includedModels and 
             obj2._meta.model_name in GeoSpatialRouting.includedModels) :
         result = None
     return result
    
  def allow_syncdb(self, db, model):
     """Do not synchronize the geospatial reference database."""

     result = None
     if model._meta.model_name in GeoSpatialRouting.includedModels :
        result = False
     return result

class DefaultRouting :
  """Routes requests to the django database interface to the geospatial
  database in order to look up intersections from the submitted latitude
  and longitude coordinates."""

  # models supported by the geospatial database
  defaultModels = set (['area', 'event', 'surveyanswer'])

  def db_for_read (self, model, **hints):
     """Selects the default database to read from."""
     return 'default'

  def db_for_write (self, model, **hints):
     """Selects the default database to write to."""
     return 'default'

  def allow_relation(self, obj1, obj2, **hints):
     """Allow any relation if a both models refer to tables in the
     geospatial database. Ideally the program would support relations 
     between multiple databases, but django does not currently allow 
     that, so the router only allows relations handled by django for
     the default database"""

     result = (obj1._meta.model_name in DefaultRouting.defaultModels and 
               obj2._meta.model_name in DefaultRouting.defaultModels)
     return result
    
  def allow_syncdb(self, db, model):
     """Allow django to synchronize the default database."""

     return True