import csv
import psycopg2
import sys

#connect to lost

conn = psycopg2.connect(dbname=sys.argv[1], host="127.0.0.1", port=5432)
cur = conn.cursor()


def export_lost():

    #users.csv
    SQL = "SELECT username, password, role_name, active FROM user_accounts JOIN roles ON role_fk = role_pk;"
    #trying using stock code to speed and clean up code:
    cur.execute(SQL)
    lost_return = cur.fetchall()
    with open("users.csv", "w") as usr_csv:
            head_row = ["username", "password", "role", "active"]
            writer = csv.DictWriter(usr_csv, fieldnames=head_row)
            writer.writeheader()

            for row in lost_return:
                writer.writerow({"username": row[0], "password": row[1], "role": row[2], "active": row[3]}) 


    #facilities.csv
    SQL = "SELECT fcode, common_name FROM facilities;"
    cur.execute(SQL)
    lost_return = cur.fetchall()

    with open("facilities.csv", "w") as facilities_csv:
            head_row = ["fcode", "common_name"]
            writer = csv.DictWriter(facilities_csv, fieldnames=head_row)
            writer.writeheader()

            for row in lost_return:
                writer.writerow({"fcode" : row[0], "common_name": row[1]}) 


    #assets.csv
    SQL = "SELECT asset_tag, description, common_name, arrive_dt, depart_dt FROM assets JOIN asset_at ON asset_pk = asset_fk JOIN facilities ON facility_fk = facility_pk;"

    cur.execute(SQL)
    lost_return = cur.fetchall()
    with open("assets.csv", "w") as assets_csv:
            head_row = ["asset_tag", "description", "facility", "acquired", "disposed"]
            writer = csv.DictWriter(assets_csv, fieldnames=head_row)
            writer.writeheader()

            for row in lost_return:
                writer.writerow({"asset_tag" : row[0], "description": row[1], "facility": row[2], "acquired": row[3], "disposed": row[4]}) 


    #transfers.csv
    SQL = "SELECT a.asset_tag, ur.username, trans.request_dt, usr.username, trans.approval_dt, fac.facility_fcode, fd.facility_fcode, t.load_dt, t.unload_dt \
    FROM transfer_requests AS trans INNER JOIN user_accounts AS ur ON trans.requester_fk=ur.user_pk INNER JOIN in_transit AS t ON t.request_fk=trans.request_pk \
    INNER JOIN user_accounts AS usr ON trans.approver_fk=usr.user_pk INNER JOIN assets AS a ON trans.asset_fk=a.asset_pk \
    INNER JOIN facilities AS fac ON trans.source_fk=fac.facility_pk  INNER JOIN facilities AS fd ON trans.dest_fk=fd.facility_pk;"
    
    cur.execute(SQL)
    lost_return = cur.fetchall()
    with open("transfers.csv", "w") as transfers_csv:
            head_row = ["asset_tag", "request_by", "request_dt", "approve_by", "approve_dt", "source", "destination", "load_dt", "unload_dt"]
            writer = csv.DictWriter(transfers_csv, fieldnames=head_row)
            writer.writeheader()

            for row in lost_return:
                writer.writerow({"asset_tag" : row[0], "request_by": row[1], "request_dt": row[2], "approve_by": row[3], "approve_dt": row[4], "source": row[5], "destination": row[6], "load_dt": row[7], "unload_dt": row[8]}) 


if __name__ == "__main__":
    export_lost()