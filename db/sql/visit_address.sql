create table visit_address 
       as select gid, geo_id, address, lfname, fcode, class, 
                 name, longitude, latitude, objectid, geom
          from address_point
          where fcode not in (100001, 114001, 115001) 
          order by longitude, latitude, gid;
alter table visit_address add primary key (gid);

                 
