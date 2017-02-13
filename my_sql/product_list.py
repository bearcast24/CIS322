import psycopg2
import sys
from CSVtoDict import *


cur = conn.cursor()

tempdict=(csv_dict("/Users/kyileleblanc/CIS322/osnap_legacy/product_list.csv"))

cur.executemany("""INSERT INTO products(vendor,description) VALUES (%(vendor)s, %(description)s)""") tempdict)