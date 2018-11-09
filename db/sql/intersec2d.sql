create table intersection2d 
       as select distinct on (longitude, latitude)
                 gid, int_id, intersec5, classifi6, classifi7, 
                 longitude, latitude, objectid, geom
          from centreline_intersection_wgs84
          order by longitude, latitude, gid;
alter table intersection2d add primary key (gid);
