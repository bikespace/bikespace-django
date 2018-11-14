#!/bin/bash

#set -e

export PGUSER="$POSTGRES_USER"
export PGPASSWORD='postgres'
OPTION=''
USER='-U postgres'
ADDR='-h db'

URI='http://opendata.toronto.ca/gcc/centreline_intersection_wgs84.zip'

psql $USER $ADDR -c "SELECT * FROM pg_available_extensions WHERE name='postgis';" | grep -q postgis
if [ $? = 0 ] ; then
   echo 'postgis extension(s) detected, ready to process'
else
   echo 'geographic data extensions to postgres must be installed'
   echo 'see http://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS23UbuntuPGSQL96Apt'
fi

sed 's/db_id/intersection/' /docker-entrypoint-initdb.d/sql/makegisdb.sql | psql $USER $ADDR
sed 's/db_id/test_intersection/' /docker-entrypoint-initdb.d/sql/makegisdb.sql | psql $USER $ADDR
curl --output centreline_intersection_wgs84.zip $URI
unzip centreline_intersection_wgs84.zip 
rm centreline_intersection_wgs84.zip
shp2pgsql -I -s 4326 CENTRELINE_INTERSECTION_WGS84.shp public.centreline_intersection_wgs84 | psql $USER $ADDR -q -d intersection 
psql $USER $ADDR -f /docker-entrypoint-initdb.d/sql/intersec2d.sql -d intersection
psql $USER $ADDR -f /docker-entrypoint-initdb.d/sql/intersection_types.sql -d intersection
shp2pgsql -I -s 4326 CENTRELINE_INTERSECTION_WGS84.shp public.centreline_intersection_wgs84 | psql $USER $ADDR -q -d test_intersection 
psql $USER $ADDR -f /docker-entrypoint-initdb.d/sql/intersec2d.sql -d test_intersection
psql $USER $ADDR -f /docker-entrypoint-initdb.d/sql/intersection_types.sql -d test_intersection
rm CENTRELINE_INTERSECTION_WGS84.*
rm CENTRELINE_INTERSECTION_WGS84_readme.txt
