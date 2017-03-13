#! /bin/bash

# Imports data from csv files to the database
# Files used: users.csv, facilities.csv, assets.csv, and transfers.csv
if [ "$#" -ne 2 ]; then
    echo "Usage: ./import_data.sh <dbname> <input dir>"
    exit;
fi

#call python scipt
python3 import_data.py $1 $2