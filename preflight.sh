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

# Database prep
cd sql
psql $1 -f create_tables.sql
curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz
tar -xzf osnap_legacy.tar.gz
bash ./import_data.sh $1 5432
rm -rf osnap_legacy osnap_legacy.tar.gz
cd ..

# Install the wsgi files
cp -R src/* $HOME/wsgi
# Need to install the crypo library as well
cp util/osnap_crypto.py $HOME/wsgi