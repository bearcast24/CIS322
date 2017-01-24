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


conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur = conn.cursor()



#product_list.csv
tempdict=(csv_dict("./osnap_legacy/product_list.csv"))
#print(tempdict)
cur.executemany("""INSERT INTO products(vendor,description) VALUES (%(vendor)s, %(description)s)""", tempdict)
#not taking the name or model, or the price.compartments
####done





#convoy.csv
tempdict=(csv_dict("./osnap_legacy/convoy.csv"))
#print(tempdict)
cur.executemany("""INSERT INTO convoys(request,depart_dt, arrive_dt) VALUES (%(transport request)s, %(depart time)s, %(arrive time)s )""", tempdict)



#transit.csv
tempdict=(csv_dict("./osnap_legacy/transit.csv"))
#print(tempdict)
cur.executemany("""INSERT INTO convoys(request,depart_dt, arrive_dt, sourse_fk, dest_fk) VALUES (%(transport request)s, %(depart date)s, %(arrive date)s, %(src facility)s, %(dst facility)s )""", tempdict)
cur.executemany("""INSERT INTO asset_on(convoy_fk, asset_fk, load_dt, unload_dt) VALUES (%(transport request)s, %(asset tag)s, %(depart time)s, %(arrive time)s )""", tempdict)
cur.executemany("""INSERT INTO asset_at(facility_fk, asset_fk, load_dt, unload_dt) VALUES (%(dst facility)s, %(asset tag)s, %(depart time)s, %(arrive time)s )""", tempdict)


#HQ_inventory.csv
tempdict=(csv_dict("./osnap_legacy/HQ_inventory.csv"))
#print(tempdict)
cur.executemany("""INSERT INTO asset_at(arrive_dt, asset_fk, facility_fk) VALUES (%(intake date)s, %(asset tag)s, HQ)""", tempdict)
cur.executemany("""INSERT INTO security_tags(asset_fk, compartment_fk) VALUES (%(asset tag)s, %(compartments)s)""", tempdict)


#DC_inventory.csv		
tempdict=(csv_dict("./osnap_legacy/DC_inventory.csv"))
#print(tempdict)
cur.executemany("""INSERT INTO asset_at(arrive_dt, asset_fk, facility_fk) VALUES (%(intake date)s, %(asset tag)s, DC)""", tempdict)
cur.executemany("""INSERT INTO security_tags(asset_fk, compartment_fk) VALUES (%(asset tag)s, %(compartments)s)""", tempdict)


#MB005_inventory.csv
tempdict=(csv_dict("./osnap_legacy/MB005_inventory.csv"))
#print(tempdict)
cur.executemany("""INSERT INTO asset_at(arrive_dt, asset_fk, facility_fk, depart_dt) VALUES (%(intake date)s, %(asset tag)s, MB, %(expunged date)s)""", tempdict)
cur.executemany("""INSERT INTO security_tags(asset_fk, compartment_fk) VALUES (%(asset tag)s, %(compartments)s)""", tempdict)


#NC_inventory.csv
tempdict=(csv_dict("./osnap_legacy/NC_inventory.csv"))	
#print(tempdict)
cur.executemany("""INSERT INTO asset_at(arrive_dt, asset_fk, facility_fk, depart_dt) VALUES (%(intake date)s, %(asset tag)s, NC, %(expunged date)s)""", tempdict)
cur.executemany("""INSERT INTO security_tags(asset_fk, compartment_fk) VALUES (%(asset tag)s, %(compartments)s)""", tempdict)


#SPNV_inventory.csv	
tempdict=(csv_dict("./osnap_legacy/SPNV_inventory.csv"))
#print(tempdict)
cur.executemany("""INSERT INTO asset_at(arrive_dt, asset_fk, facility_fk) VALUES (%(intake date)s, %(asset tag)s, SPNV)""", tempdict)
cur.executemany("""INSERT INTO security_tags(asset_fk, compartment_fk) VALUES (%(asset tag)s, %(compartments)s)""", tempdict)




#security_compartments.csv
tempdict=(csv_dict("./osnap_legacy/security_compartments.csv"))
#print(tempdict)
cur.executemany("""INSERT INTO levels(abbrv,comment) VALUES (%(compartment_tag)s, %(compartment_desc)s)""", tempdict)	
#done


#security_levels.csv
tempdict=(csv_dict("./osnap_legacy/security_levels.csv"))
#print(tempdict)
cur.executemany("""INSERT INTO levels(abbrv,comment) VALUES (%(level)s, %(description)s)""", tempdict)	
###done??


#vendors.csv
tempdict=(csv_dict("./osnap_legacy/vendors.csv"))
#print(tempdict)


#Not used....



#acquisitions.csv
tempdict=(csv_dict("./osnap_legacy/acquisitions.csv"))
#print(tempdict)
cur.executemany("""INSERT INTO asset_at(asset_fk, arrive_dt) VALUES (%(asset tag)s, %(arrive date)s)""", tempdict)	






# commit the changes to the database
conn.commit()

# close the connection nicely
cur.close()
conn.close()