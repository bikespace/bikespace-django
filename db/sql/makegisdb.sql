CREATE DATABASE db_id;
\connect db_id;

CREATE SCHEMA postgis;
ALTER DATABASE db_id SET search_path=public, postgis, contrib;
\connect db_id;
CREATE EXTENSION postgis SCHEMA postgis;
SELECT postgis_full_version();

CREATE DATABASE bike_parking;

GRANT ALL PRIVILEGES ON DATABASE bike_parking to postgres;
