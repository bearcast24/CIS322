Contained files:

create_tables.sql - a SQL script to create the LOST database tables

import_data.sh - a Bash script file to download legacy data, and import using the import_data.py (TAKES: port and database)

import_data.py - a python script that makes each CSV file into a dictionary and adds to the provided database. (TAKES: port and database)



Usage: 

$ createdb lost

$ psql lost -f create_tables.sql 

$ bash import_data.sh lost 5432


>Then call the lost database with 
$ psql lost















Expecting these files from OSNAP

Files:
security_levels.csv - An ordered listing of security levels. 'u' is the lowest security level and 'z' is the highest security level.

security_compartments.csv - A listing of security compartments. The actual descriptions have been redacted but LOST will be expected to allow a comment or description for each compartment.

vendors.csv - A listing of vendors which are on the OSNAP vendor list and have open purchasing agreements.

product_list.csv - A listing of products with their associated vendor.

acquisitions.csv - A listing of items purchased.

transit.csv - Samples from the spreadsheets currently used for tracking transit requests.

convoy.csv - Samples of the current way convoys are tracked for moving assets.

DC_inventory.csv - Inventory from the DC facility

HQ_inventory.csv - Inventory from the HQ facility

MB005_inventory.csv - Inventory from the MB005 facility

NC_inventory.csv - Inventory from the National City facility

SPNV_inventory.csv - Inventory from the Sparks Nevada facility