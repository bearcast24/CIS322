CREATE TABLE roles (
	role_pk	serial primary key,
	role_name varchar(32) --could be long title
);
--Using a role table gives growth potenial, as well as merdging jobs as needed

CREATE TABLE user_accounts (
	user_pk serial primary key,
	username varchar (16), --usernames no more than 16 chars
	password varchar (16),  --passwords no more than 16 chars
	role_fk integer REFERENCES roles(role_pk) --users can only have one role at this point
);

--Comms:
-- I'd rather have numbering for users than have to add keys later, building ahead.
-- The code fufills the requsted output with usernames and PW that are no more than 16 chars
-- One table makes sense at this point. Each user has one user-ID and PW




CREATE TABLE assets (
	asset_pk serial primary key,
	asset_tag varchar(16), 
	description text,
	disposed boolean
);

CREATE TABLE facilities (
	facility_pk serial primary key,
	fcode varchar(6),
	common_name varchar(32)
);


CREATE TABLE asset_at (
	asset_fk integer REFERENCES assets(asset_pk),
	facility_fk integer REFERENCES facilities(facility_pk),
	arrive_dt timestamp,
	depart_dt timestamp DEFAULT NULL --Better to mark it NULL, just incase an import goes crazy
);

-- The assest locations are in asset_at and to facilities table by the asset_fk and facility_fk




-- Test Roles:

-- INSERT INTO roles (role_name) VALUES ('Logistics Officer');

-- INSERT INTO roles (role_name) VALUES ('Facilities Officer');