CREATE TABLE user (
		user_pk serial primary key,
		username varchar (16), --usernames no more than 16 chars
		password varchar (16)  --passwords no more than 16 chars
	);

--Comms:
-- I'd rather have numbering for users than have to add keys later, building ahead.
-- The code fufills the requsted output with usernames and PW that are no more than 16 chars
-- One table makes sense at this point. Each user has one user-ID and PW
