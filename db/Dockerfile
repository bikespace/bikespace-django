# base image
FROM mdillon/postgis

COPY ./mkintersectiondb.sh /docker-entrypoint-initdb.d/qmkintersectiondb.sh
COPY ./sql /docker-entrypoint-initdb.d/sql/

RUN chmod +x /docker-entrypoint-initdb.d/qmkintersectiondb.sh