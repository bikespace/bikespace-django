# base image
FROM mdillon/postgis

# set working directory
WORKDIR /usr/src/app

COPY ./mkintersectiondb.sh /usr/src/app/mkintersectiondb.sh
COPY ./sql /usr/src/app
RUN chmod +x /usr/src/app/mkintersectiondb.sh

CMD ["/usr/src/app/mkintersectiondb.sh"]