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


cd sql
psql $1 -f create_tables.sql
cd ..


# Install the wsgi files
cp -R src/* $HOME/wsgi