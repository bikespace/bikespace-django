!/bin/sh

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