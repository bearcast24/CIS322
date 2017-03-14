import csv
import psycopg2
import sys

#connect to lost
conn = psycopg2.connect(dbname=sys.argv[1], host="127.0.0.1", port=5432)
cur = conn.cursor()
#Cmd line grab of path:
file_path = sys.argv[2]


#using small functions to prevent break of one large main loop

def import_users(users_file):
    with open(users_file, "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for item in reader:
            #Check role
            SQL = "SELECT role_pk FROM roles WHERE role_name = %s;"
            cur.execute(SQL,(item['role'],) )
            res = cur.fetchall()

            if not res:
                SQL = "INSERT INTO roles (role_name) VALUES (%s) RETURNING role_pk;"
                cur.execute(SQL,(item['role'],) )
                role_key = cur.fetchone()[0]
            role_key=res[0]

            #Make user:
            SQL = "INSERT INTO user_accounts (username, password, active, role_fk) VALUES(%s, %s, %s, %s);"
            cur.execute(SQL, (item['username'], item['password'], item['active'], role_key))
            conn.commit() #Save after each user is added


            

def import_facilities(facilities_file):
    with open(facilities_file, "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for item in reader:
            SQL = "INSERT INTO facilities (fcode, common_name) VALUES(%s,%s);"
            cur.execute(SQL, (item['fcode'], item['common_name']))
            conn.commit()



def import_assets(assets_file):
    with open(assets_file, "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for item in reader:
            SQL = "INSERT INTO assets (asset_tag, description) VALUES( %s, %s ) RETURNING asset_pk;"
            cur.execute(SQL, (item['asset_tag'], item['description']))
            asset_pk = cur.fetchone()[0]
            
            SQL2 = "SELECT facility_pk FROM facilities WHERE fcode= %s;"
            cur.execute(SQL2, (item['facility'],))
            facility_pk = cur.fetchone()[0]


            SQL3 = "INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt, dispose_dt)  VALUES (%s, %s, %s, %s);"
            if item['disposed'] == 'NULL':
                cur.execute(SQL3, (asset_pk, facility_pk, item['acquired'], None))
            else:
                cur.execute(SQL3, (asset_pk, facility_pk, item['acquired'], item['disposed']))
            
            conn.commit() #One save per item



def import_transfers(transfers_file):
    with open(transfers_file, "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for line in reader:
            #Get user keys for items in transit
            cur.execute("SELECT user_pk FROM user_accounts WHERE username = {}".format(line['request_by']))
            reqr = cur.fetchone()[0]
            cur.execute("SELECT user_pk FROM user_accounts WHERE username = {}".format(line['approve_by']))
            appr = cur.fetchone()[0]
            
            #Facility key identifier for source and destination
            cur.execute("SELECT facility_pk FROM facilities WHERE fcode = {}".format(line['source']))
            src = cur.fetchone()[0]
            cur.execute("SELECT facility_pk FROM facilities WHERE fcode = {}".format(line['destination']))
            dest = cur.fetchone()[0]

            #Asset key:
            cur.execute("SELECT asset_pk FROM assets WHERE asset_tag = {}".format(line['asset_tag']))
            asset_pk = cur.fetchone()[0]
            
            #Insert data into transfer requests table
            SQL = "INSERT INTO transfer_requests (requestor_fk, request_dt, source_fk, dest_fk, asset_fk, approver_fk, approval_dt) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur.execute(SQL, (reqr, line['request_dt'], src, dest, asset_pk, appr, line['approve_dt']))

            #Insert data for in_transit table
            SQL = "INSERT INTO in_transit (asset_fk, source_fk, dest_fk, load_dt, unload_dt) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(SQL, (asset_pk, src, dest, line['load_dt'], line['unload_dt']))
            conn.commit()


if __name__ == "__main__":
    #These two must run first, assets depend on them
    import_users('{}/users.csv'.format(file_path))
    import_facilities('{}/facilities.csv'.format(file_path))
    ####
    import_assets('{}/assets.csv'.format(file_path))
    import_transfers('{}/transfers.csv'.format(file_path))