# import psycopg2
import sys
import csv

def csv_dict(file):
    with open(file) as csvfile:
        asset_list = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            asset_list.append(row)
        return asset_list





# conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
# cur = conn.cursor()


#DC_inventory.csv		
tempdict=(csv_dict("./osnap_legacy/DC_inventory.csv"))
print(tempdict)
#convoy.csv
tempdict=(csv_dict("./osnap_legacy/convoy.csv"))
print(tempdict)


#HQ_inventory.csv
tempdict=(csv_dict("./osnap_legacy/HQ_inventory.csv"))
print(tempdict)

#product_list.csv
tempdict=(csv_dict("./osnap_legacy/product_list.csv"))
print(tempdict)
#cur.executemany("""INSERT INTO products(vendor,description) VALUES (%(vendor)s, %(description)s)""") tempdict)

#MB005_inventory.csv
tempdict=(csv_dict("./osnap_legacy/MB005_inventory.csv"))
print(tempdict)

#security_compartments.csv
tempdict=(csv_dict("./osnap_legacy/security_compartments.csv"))
print(tempdict)

#NC_inventory.csv
tempdict=(csv_dict("./osnap_legacy/NC_inventory.csv"))	
print(tempdict)

#security_levels.csv
tempdict=(csv_dict("./osnap_legacy/security_levels.csv"))
print(tempdict)
	
#transit.csv
tempdict=(csv_dict("./osnap_legacy/transit.csv"))
print(tempdict)

#SPNV_inventory.csv	
tempdict=(csv_dict("./osnap_legacy/SPNV_inventory.csv"))
print(tempdict)

#vendors.csv
tempdict=(csv_dict("./osnap_legacy/vendors.csv"))
print(tempdict)

#acquisitions.csv
tempdict=(csv_dict("./osnap_legacy/acquisitions.csv"))
print(tempdict)





# # commit the changes to the database
# conn.commit()

# # close the connection nicely
# cur.close()
# conn.close()