#! /usr/bin/bash

#Kyile LeBlanc
#W3 
#CIS 322

# Goals:
#    1. creates the database

if [ "$#" -ne 1 ]; then
    echo "Usage: ./preflight.sh <dbname>"
    exit;
fi

# Database prep
# All that this preflight script needs to do is set up the db
# Andy's script already drops and creates db

	# psql $1 -f create_tables.sql
	# curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz
	# tar -xzf osnap_legacy.tar.gz
	# bash ./import_data.sh $1 5432
	# rm -rf osnap_legacy osnap_legacy.tar.gz

cd sql
psql $1 -f create_tables.sql
cd ..


# Install the wsgi files
cp -R src/* $HOME/wsgi