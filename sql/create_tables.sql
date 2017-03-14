CREATE TABLE roles (
	role_pk	serial primary key,
	role_name varchar(32) --could be long title
);
--Using a role table gives growth potenial, as well as merdging jobs as needed

CREATE TABLE user_accounts (
	user_pk serial primary key,
	username varchar (16), --usernames no more than 16 chars
	password varchar (16),  --passwords no more than 16 chars
	active boolean DEFAULT TRUE,
	role_fk integer REFERENCES roles(role_pk) --users can only have one role at this point
);

--Comms:
-- I'd rather have numbering for users than have to add keys later, building ahead.
-- The code fufills the requsted output with usernames and PW that are no more than 16 chars
-- One table makes sense at this point. Each user has one user-ID and PW


INSERT INTO roles (role_name) VALUES ('Logistics Officer');

INSERT INTO roles (role_name) VALUES ('Facilities Officer');

--Make the two required roles now to save the blank or nonexsiting role problem



CREATE TABLE assets (
	asset_pk serial primary key,
	asset_tag varchar(16), 
	description text,
	disposed timestamp DEFAULT null
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
	dispose_dt timestamp DEFAULT NULL,
	depart_dt timestamp DEFAULT NULL --Better to mark it NULL, just incase an import goes crazy
);

-- The assest locations are in asset_at and to facilities table by the asset_fk and facility_fk

CREATE TABLE transfer_requests (
	request_pk serial primary key,
	requester_fk integer REFERENCES user_accounts (user_pk),
	request_dt timestamp,
	source_fk integer REFERENCES facilities (facility_pk),
	dest_fk	integer REFERENCES facilities (facility_pk),
	asset_fk integer REFERENCES assets (asset_pk),
	approver_fk integer REFERENCES user_accounts (user_pk),
	approval_dt timestamp
);

/*A transfer minimally has:
A requester, a logistics officer submitting the request.
The date and time the transfer request was submitted.
The source facility.
The destination facility.
The asset to be transfered.
An approver, a facilities officer approving the transfer request.
The date and time the transfer request was approved.*/

--transfer_requests is a many to many table pulling in several of the core database records to track

CREATE TABLE in_transit (
	asset_fk integer REFERENCES assets (asset_pk),
	request_fk integer REFERENCES transfer_requests (request_pk),
	source_fk integer REFERENCES facilities(facility_pk),
	dest_fk integer REFERENCES facilities(facility_pk),
	load_dt timestamp,
	unload_dt timestamp
);

 -- tracks which user set the load and unload times via the transfer_requests table
 