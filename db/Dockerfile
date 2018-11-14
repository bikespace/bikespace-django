# base image
FROM mdillon/postgis

RUN apt-get update \
    && apt-get install -y curl zip \
    && apt-get clean

RUN curl --output /tmp/centreline_intersection_wgs84.zip 'http://opendata.toronto.ca/gcc/centreline_intersection_wgs84.zip'
RUN unzip /tmp/centreline_intersection_wgs84.zip -d /tmp
RUN rm /tmp/centreline_intersection_wgs84.zip

COPY ./mkintersectiondb.sh /docker-entrypoint-initdb.d/qmkintersectiondb.sh
COPY ./sql /docker-entrypoint-initdb.d/sql/
RUN chmod +x /docker-entrypoint-initdb.d/qmkintersectiondb.sh
