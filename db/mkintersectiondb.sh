#!/bin/sh

set -e

export PGUSER="$POSTGRES_USER"
export PGPASSWORD='postgres'
OPTION=''

URI='http://opendata.toronto.ca/gcc/centreline_intersection_wgs84.zip'

psql $USER $ADDR -c "SELECT * FROM pg_available_extensions WHERE name='postgis';" | grep -q postgis
if [ $? = 0 ] ; then
   echo 'postgis extension(s) detected, ready to process'
else
   echo 'geographic data extensions to postgres must be installed'
   echo 'see http://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS23UbuntuPGSQL96Apt'
fi

sed 's/db_id/intersection/' /docker-entrypoint-initdb.d/sql/makegisdb.sql | psql
sed 's/db_id/test_intersection/' /docker-entrypoint-initdb.d/sql/makegisdb.sql | psql

shp2pgsql -I -s 4326 /tmp/CENTRELINE_INTERSECTION_WGS84.shp public.centreline_intersection_wgs84 | psql -q -d intersection 

psql -f /docker-entrypoint-initdb.d/sql/intersec2d.sql -d intersection
psql -f /docker-entrypoint-initdb.d/sql/intersection_types.sql -d intersection

shp2pgsql -I -s 4326 /tmp/CENTRELINE_INTERSECTION_WGS84.shp public.centreline_intersection_wgs84 | psql -q -d test_intersection 

psql -f /docker-entrypoint-initdb.d/sql/intersec2d.sql -d test_intersection
psql -f /docker-entrypoint-initdb.d/sql/intersection_types.sql -d test_intersection
