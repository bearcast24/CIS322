--Asset Tables

CREATE TABLE products (
product_pk	integer primary key, 
vendor text, 
description text, 
alt_description text
);




CREATE TABLE assets (
	asset_pk 	integer primary key, 
	product_fk 	integer REFERENCES products(product_pk), 
	asset_tag 	text, 
	description text, 
	alt_description text
	);

CREATE TABLE vehicles (
vehicle_pk integer primary key,
asset_fk integer REFERENCES assets(asset_pk),
);

CREATE TABLE facilities (
facility_pk integer primary key,
fcode varchar(6),
common_name text,
location text
);


CREATE TABLE asset_at (
asset_fk integer REFERENCES assets(asset_pk) ,
facility_fk integer REFERENCES facilities(facility_pk),
arrive_dt timestamp,
depart_dt timestamp
);


CREATE TABLE convoys (
convoy_pk integer primary key,
request text,
source_fk integer REFERENCES facilities(facility_pk),
dest_fk integer REFERENCES facilities(facility_pk),
depart_dt timestamp,
arrive_dt timestamp
);



CREATE TABLE used_by (
vehicle_fk integer REFERENCES vehicles(vehicle_pk),
convoy_fk integer  REFERENCES vehicles(vehicle_pk),
);

 
CREATE TABLE asset_on (
asset_fk integer  REFERENCES facilities(facility_pk),
convoy_fk integer REFERENCES convoys(convoy_pk),
load_dt timestamp,
unload_dt timestamp
);


--User Tables

CREATE TABLE users (
user_pk integer primary key,
username text,
active boolean
);


CREATE TABLE roles (
role_pk integer primary key,
title text
);




CREATE TABLE user_is (
user_fk integer REFERENCES users(user_pk),
role_fk integer REFERENCES roles(role_pk)
);

CREATE TABLE user_supports (
user_fk integer     REFERENCES users(user_pk),
facility_fk integer REFERENCES facilities(facility_pk)
);






--Security Tables

CREATE TABLE levels (
level_pk integer primary key,
abbrv text,
comment text
);


CREATE TABLE compartments (
compartment_pk integer primary key,
abbrv text,
comment text
);
 
CREATE TABLE security_tags (
tag_pk integer primary key,
level_fk integer    not null        REFERENCES levels(level_pk),
compartment_fk integer    not null  REFERENCES compartments(compartment_pk),
user_fk integer     REFERENCES users(user_pk),
product_fk integer  REFERENCES products(product_pk),
asset_fk integer    REFERENCES assets(asset_pk)
);

--Security tags must have both level and compartment. Security tags must also have a user xor product xor asset.















