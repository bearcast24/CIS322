import psycopg2
import sys
import csv

def csv_dict(file):
    with open(file) as csvfile:
        asset_list = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            asset_list.append(row)
        return asset_list





conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()


#DC_inventory.csv		


#convoy.csv




#HQ_inventory.csv



#product_list.csv
tempdict=(csv_dict("./osnap_legacy/product_list.csv"))

cur.executemany("""INSERT INTO products(vendor,description) VALUES (%(vendor)s, %(description)s)""") tempdict)

#MB005_inventory.csv

#security_compartments.csv

#NC_inventory.csv	

#security_levels.csv

	
#transit.csv

#SPNV_inventory.csv	

#vendors.csv

#acquisitions.csv


# commit the changes to the database
conn.commit()

# close the connection nicely
cur.close()
conn.close()