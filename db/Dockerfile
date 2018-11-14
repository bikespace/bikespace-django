# base image
FROM mdillon/postgis

RUN apt-get update \
    && apt-get install -y curl zip \
    && apt-get clean

COPY ./mkintersectiondb.sh /docker-entrypoint-initdb.d/q_mkintersectiondb.sh
COPY ./sql /docker-entrypoint-initdb.d/sql/
RUN chmod +x /docker-entrypoint-initdb.d/q_mkintersectiondb.sh

#CMD ["/docker-entrypoint-initdb.d/q_mkintersectiondb.sh"]