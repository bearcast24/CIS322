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
cd sql
psql $1 -f create_tables.sql