#!/bin/bash

# set local variables
URL=$1
DB_NAME=hw
PORT=5432

# set the path
# (I pass this script to the VM from another script running on my host
#  machine ... this isn't necessary if calling this script directly on the VM)
# PATH=/osnap/bin:$PATH

# create db
createdb -p $PORT $DB_NAME

# pull student repo
git clone $URL CIS322
cd CIS322

# run preflight
. preflight.sh $DB_NAME

# get config file from ix (database name is 'hw')
cd src
curl -O http://ix.cs.uoregon.edu/~hampton2/322/lost_config.json

# also copy config to wsgi folder
cp lost_config.json ~/wsgi/
