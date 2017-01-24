#create_tables.sql
#Kyile LeBlanc
#CIS 322 #2

#Use python to make tables from the project guidelines


##Asset Tables

CREATE TABLE products (
product_pk	integer primary key, 
vendor text, 
description text, 
alt_description text
);




CREATE TABLE assets (
	asset_pk 	integer primary key, 
	product_fk 	integer, 
	asset_tag 	text, 
	description text, 
	alt_description text
	);

CREATE TABLE vehicles
vehicle_pk integer primary key,
asset_fk integer,
);

CREATE TABLE facilities (
facility_pk integer primary key,
fcode varchar(6),
common_name text,
location text
);


CREATE TABLE asset_at (
asset_fk integer,
facility_fk integer,
arrive_dt timestamp,
depart_dt timestamp
);


CREATE TABLE convoy (
convoy_pk integer primary key,
request text,
source_fk integer,
dest_fk integer,
depart_dt timestamp,
arrive_dt timestamp
);



CREATE TABLE used_by (
vehicle_fk integer,
convoy_fk integer,
);

 
CREATE TABLE asset_on (
asset_fk integer,
convoy_fk integer,
load_dt timestamp,
unload_dt timestamp
);


##User Tables

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
user_fk integer,
role_fk integer
);

CREATE TABLE user_supports (
user_fk integer,
facility_fk integer
);






##Security Tables

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
level_fk integer    not null,
compartment_fk integer    not null,
user_fk integer,
product_fk integer,
asset_fk integer
);

##Security tags must have both level and compartment. Security tags must also have a user xor product xor asset.















