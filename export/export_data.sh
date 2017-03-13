#! /bin/bash

# Exports data in LOST to csv files
# Creates:, users.csv, facilities.csv, assets.csv, and transfers.csv
if [ "$#" -ne 2 ]; then
	echo "Usage: ./export_data.sh <dbname> <output dir>"
	exit;
fi

#Creates new folder, no mater what was there:
rm -rf $2
mkdir $2

#Run python to export data into CSV
python3 export_data.py $1

#Move files to location:
mv *.csv $2