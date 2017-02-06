#! /usr/bin/bash

#Kyile LeBlanc
#W3 
#CIS 322

#Calling program:
#bash ./preflight.sh lost
# Goals:
#    1. creates the database
#    2. imports the legacy data <-Sort of
#    3. Copies the source files to $HOME/wsgi to serve webapp

if [ "$#" -ne 1 ]; then
    echo "Usage: ./preflight.sh <dbname>"
    exit;
fi

# Make Database
cd sql
psql -f create_tables.sql $1 
psql -f import_data.sql $1 -p5432
cd ..

# Install the wsgi files
cp -R src/* $HOME/wsgi