#!/bin/bash

OPTION=''
USER='-U postgres'
ADDR='-h 127.0.0.1'
URI='http://opendata.toronto.ca/gcc/centreline_intersection_wgs84.zip'
INVALID_OPTION=''
for ARGUMENT do 
   if [ -n "$OPTION" ]; then
      case $OPTION in
         '--user' | '-U'   )  USER="-U $ARGUMENT";;
         '--target' | '-t' )  ADDR="-h $ARGUMENT";;
         '--source' | '-s' )  URI=$ARGUMENT;;
         *                 )  INVALID_OPTION=$OPTION
      esac
      OPTION=''
   else
      OPTION=$ARGUMENT
   fi
done

if [ -n "$INVALID_OPTION" ]; then
   echo "$INVALID_OPTION is invalid"
   exit 1
elif [ -n "$OPTION" ]; then
   echo "$OPTION has no value or is invalid"
   exit 1
fi

psql $USER $ADDR -c 'SELECT * FROM pg_available_extensions;' | grep -q postgis
if [ $? = 0 ] ; then
   echo 'postgis extension(s) detected, ready to process'
else
   echo 'geographic data extensions to postgres must be installed'
   echo 'see http://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS23UbuntuPGSQL96Apt'
fi

sed 's/db_id/intersection/' sql/makegisdb.sql | psql $USER $ADDR
sed 's/db_id/test_intersection/' sql/makegisdb.sql | psql $USER $ADDR
curl --output centreline_intersection_wgs84.zip $URI
unzip centreline_intersection_wgs84.zip 
rm centreline_intersection_wgs84.zip
shp2pgsql -I -s 4326 CENTRELINE_INTERSECTION_WGS84.shp public.centreline_intersection_wgs84 | psql $USER $ADDR -q -d intersection 
psql -U postgres -h 127.0.0.1 -f sql/intersec2d.sql -d intersection
psql -U postgres -h 127.0.0.1 -f sql/intersection_types.sql -d intersection
shp2pgsql -I -s 4326 CENTRELINE_INTERSECTION_WGS84.shp public.centreline_intersection_wgs84 | psql $USER $ADDR -q -d test_intersection 
psql $USER $ADDR -f sql/intersec2d.sql -d test_intersection
psql $USER $ADDR -f sql/intersection_types.sql -d test_intersection
rm CENTRELINE_INTERSECTION_WGS84.*
rm CENTRELINE_INTERSECTION_WGS84_readme.txt
