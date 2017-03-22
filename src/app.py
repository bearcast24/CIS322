from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
import datetime
import sys
import json
#This should pull all configuations from the json file:
from config import dbname, dbhost, dbport

app = Flask(__name__)

app.secret_key = 'secret_password'

#Enter and Exit LOST
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET': #Need to store login state??
        return render_template('login.html')

    if request.method == 'POST':
        uname = request.form['username']        
        pwd = request.form['password']
        #Connect to postgres:
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        #queries:
        cur.execute("SELECT username, password, role_name, active FROM user_accounts INNER JOIN roles ON role_pk = role_fk \
            WHERE username = '{}' and password = '{}';".format(uname, pwd))

        result = cur.fetchone()
        #If user is found:
        if result is not None:
            session['username'] = uname
            session['role'] = result[2]
            if result[3]:
                session['logged_in'] = True
                #send to Dashboard after getting signed in
                return redirect(url_for('dashboard'))
            else:
                session['logged_in'] = False
                return render_template('access_denied.html')
        #If no user is found:
        return render_template('no_user.html')


    return render_template('login.html')   


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session['logged_in']:
        #test for logged in session and redirect
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        #Hard code for ease-> should use database to make avail forms

        


        #Logistics
        if session['role'] == "Logistics Officer":
            tasks = []
            #listing of asset transits which need to have load or unload times set
            cur.execute("SELECT request_fk, load_dt, unload_dt FROM in_transit WHERE load_dt IS NULL OR unload_dt IS NULL;")
            todo_request = cur.fetchall()

            for item in todo_request:
                item_que = dict()
                item_que["request_fk"] =item[0]
                item_que["load_dt"] =item[1]
                item_que["unload_dt"] =item[2]
                tasks.append(item_que)
            #Send to Flask
            session['tasks'] = tasks


        #Facilities
        elif session['role'] == "Facilities Officer":
            tasks = []
            #listing of transfer requests needing approval.
            cur.execute("SELECT request_pk, user_accounts.username, transfer_requests.request_dt FROM transfer_requests INNER JOIN \
                    user_accounts ON transfer_requests.requester_fk = user_accounts.user_pk WHERE approval_dt IS NULL;") 
                    #https://www.w3schools.com/sql/sql_join_inner.asp
            todo_request = cur.fetchall()

            for item in todo_request:
                item_que = dict()
                item_que["request_pk"] =item[0]
                item_que["requester"] =item[1]
                item_que["request_time"] =item[2]
                tasks.append(item_que)
            session['tasks'] = tasks
        





            SQL = "SELECT * FROM requests WHERE approval_dt IS NULL"
            cur.execute(SQL)
            res = cur.fetchall()
            keys = ('request_pk', 'requestor', 'request_dt', 'src_fac', 'dest_fac', 'asset', 'approver', 'approval_date')
            unapproved = [dict(zip(keys, r)) for r in res]
            return unapproved







        #Save asset changes
        conn.commit()
        return render_template('dashboard.html');
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['logged_in'] = False #Terminate the session
    #logout_user()
    session.clear()
    return redirect(url_for('login'))





#@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    
    elif request.method == 'POST':
        uname = request.form['username']        
        pwd = request.form['password']
        rol = request.form['role']

        session['username'] = uname
        #Connect to postgres:
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        #queries:
        #Is user in DB?
        cur.execute("SELECT username, password FROM user_accounts where username = '{}' AND password = '{}';".format(uname, pwd))
        USER_here = cur.fetchone()

        #Is role in DB or need to be made?
        cur.execute("SELECT role_pk from roles where role_name = '{}';".format(rol))
        ROLE_here = cur.fetchone()

        #Cool idea on how to add roles from conversations. Once roles are set, then lookups won't be needed to write new ones
        if not ROLE_here:
            cur.execute("INSERT INTO roles (role_name) VALUES ('{}') RETURNING role_pk;".format(rol))
            rol_key = cur.fetchone()[0] #grab the key for the new role
            conn.commit()
        else:
            rol_key = ROLE_here[0]

        #logic:
        #user is in user table:
        if USER_here is not None:
            return render_template('user_exists.html')
        else: 
            cur.execute("INSERT INTO user_accounts(username,password, role_fk) VALUES ('{}', '{}', '{}');".format(uname, pwd, rol_key))
            conn.commit()
            return render_template('user_added.html')


@app.route('/activate_user', methods = ['POST']) #only post requests
def activate_user():
    #Connect to postgres:
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()

    uname = request.form['username']        
    pwd = request.form['password']
    rol = request.form['role']
    SQL = "SELECT username, password, role_fk, active FROM user_accounts WHERE username = %s"
    cur.execute(SQL, (uname,))
    user_return = cur.fetchall()

    ##Make or update user:
    #Make new user:
    if not user_return:
        #find roles
        SQL = "SELECT role_pk from roles WHERE role_name = %s"
        cur.execute(SQL,(rol,))
        role_key = cur.fetchone()[0]

        #add to user db
        SQL = "INSERT INTO user_accounts (username, password, role_fk, active) VALUES (%s, %s, %s, %s)"
        cur.execute(SQL, (uname, pwd, role_key, True ))
        conn.commit() # Save the new entry

        #Pass back feedback:
        return "The user {} was successfully added to the database and activated as a {}".format(uname, rol)

    #Update user:
    else: 
        #The user was found and wants a new password
        cur.execute('UPDATE user_accounts SET password=%s, active=%s WHERE username=%s;', (pwd, True, uname))
        conn.commit() # Save
        #Return message of change:
        return "The {} user {} was updated in the database and activated".format(rol, uname)


@app.route('/revoke_user', methods = ['POST']) #only post requests
def revoke_user():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    #No need to test is user is real as it is only deactivating accounts, if it did respond that a user was not found
    #it could be a security issue
    uname = request.form['username']
    cur.execute('UPDATE user_accounts SET active=%s WHERE username=%s;', (False, uname))
    conn.commit() #Save the update, event if nothing exists
    return 'User {} has been updated'.format(uname)


#New pages:

@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
    if not session['logged_in']:
        return redirect(url_for('login'))
    #Connect to postgres:
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
    #make a dict of facity:
    cur.execute("SELECT * FROM facilities;")
    res = cur.fetchall()
    fac_results = []
    for line in res:
        fac = dict()
        #line[0] = key
        fac['common_name'] = line[1]
        fac['fcode'] = line[2]
        fac_results.append(fac)
    session['fac_results'] = fac_results

    #show pages
    if request.method == 'GET':
        return render_template('add_facility.html')

    if request.method == 'POST':
        common_name = request.form['common_name']
        code = request.form['fcode']
        #chedk for fac before adding:
        cur.execute("SELECT fcode, common_name from facilities WHERE fcode = %s AND common_name = %s;",(code, common_name))
        res_fac = cur.fetchall()
        #add new
        if not res_fac: 
            cur.execute("INSERT INTO facilities (common_name, fcode) VALUES (%s, %s);", (common_name,code))
            conn.commit()
            return redirect(url_for('add_facility'))
        else: 
            return render_template('error_duplicate.html')


@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    if not session['logged_in']:
        return redirect(url_for('login'))
    #Connect to postgres:
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
    
    #Make asset list for page:
    cur.execute("SELECT * FROM assets;")
    asset_ret = cur.fetchall()
    asset_results = []
    #should use list comp for clairty:
    for line in asset_ret:
        data = dict()
        #line[0] = key
        data['asset_tag'] = line[1]
        data['description'] = line[2]
        asset_results.append(data)
    session['asset_list'] = asset_results
    
    #Make fac list for page
    cur.execute("SELECT common_name from facilities;")
    res = cur.fetchall()
    session['active_fac'] = [row[0] for row in res]

    if request.method == 'GET':
        return render_template('add_asset.html')

    elif request.method == 'POST':
        asset_tag = request.form['asset_tag']
        desc = request.form['description']
        fac = request.form['common_name']
        arrive_dt = request.form['date']

        #DB check:
        cur.execute("SELECT asset_tag from assets WHERE asset_tag = %s;", (asset_tag,))
        asset_there = cur.fetchall()

        if not asset_there:
            cur.execute("INSERT INTO assets (asset_tag, description) VALUES (%s, %s) RETURNING asset_pk;", (asset_tag, desc))
            asset_pk = cur.fetchone()[0]
            conn.commit()

            #Find asset home:
            cur.execute("SELECT facility_pk FROM facilities WHERE common_name='{}';".format(fac))
            facility_pk = cur.fetchone()[0]

            #Give asset the home it disserves:
            cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES (%s, %s, %s);", (asset_pk, facility_pk, arrive_dt))
            conn.commit()
            return redirect(url_for('add_asset'))
        #Chance are it is a spelling or case issue:   
        else:        
            return render_template('error_duplicate.html')



# #Access might be broken: Something janky is happening:
@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
    if not session['logged_in']:
        return redirect(url_for('login'))

    if session['role'] == 'Logistics Officer':
        #print(session['role'])
        #Connect to postgres:
        #Page fun:
        if request.method == 'GET':
            return render_template('dispose_asset.html')
        #Req page:
        if request.method == 'POST':
            conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
            cur  = conn.cursor()
            ass_tag = request.form['asset_tag']
            d_day = request.form['disposed_dt']
            cur.execute("SELECT asset_tag, disposed from assets WHERE asset_tag LIKE %s;",(ass_tag,))
            ret_assets = cur.fetchall()

            #item not there:
            if not ret_assets:
                return render_template('error_removed.html')
            #Remove item: (Need to add in way to see item alreeady removed)
            else: 
                cur.execute("UPDATE assets SET disposed = %s where asset_tag = %s;",(d_day, ass_tag))
                conn.commit()
                return render_template('dashboard.html')
    else:
        return render_template('access_denied.html')



@app.route('/asset_report', methods=['GET', 'POST'])
def asset_report():
    if not session['logged_in']:
        return redirect(url_for('login'))
    
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
    cur.execute("SELECT common_name from facilities;")
    res = cur.fetchall()
    session['active_fac'] = [row[0] for row in res]
   
    if request.method == 'GET':
        return render_template('asset_report.html')

    elif request.method =='POST':
        time = request.form['date']
        fac = request.form['common_name']

        cur.execute("SELECT asset_tag, description, common_name, arrive_dt, disposed FROM assets \
            JOIN asset_at ON assets.asset_pk = asset_at.asset_fk \
            JOIN facilities ON asset_at.facility_fk = facilities.facility_pk \
            WHERE common_name LIKE %s AND arrive_dt = %s;",(fac, time))
        repo = cur.fetchall()

        asset_results = []
        for line in repo:
            data = dict()
            #line[0] = key
            data['asset_tag'] = line[0]
            data['description'] = line[1]
            data['common_name'] = line[2]
            data['arrive_dt'] = line[3]
            data['disp_dt'] = line[4]
            asset_results.append(data)
        session['asset_repo'] = asset_results

        return redirect(url_for('asset_report'))


#8
@app.route('/transfer_req', methods = ['GET', 'POST'])
def transfer_req():
    if not session['logged_in']:
        return redirect(url_for('login'))

    if session['role'] != 'Logistics Officer':
        return render_template('access_denied.html')

    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()

    if request.method == 'POST':

        tag = request.form['asset_tag']
        source = request.form['source_fcode']
        dest = request.form['dest_fcode']
        request_dt = str(datetime.datetime.now())

        #sql
        cur.execute("SELECT asset_pk FROM assets WHERE asset_tag=%s;",(tag,))
        repo = cur.fetchone()
        if not repo:
            asset_fk = repo[0]
        return render_template('tag_missing.html')


        cur.execute("SELECT facility_pk FROM facilities WHERE fcode= %s;",(source,))
        repo = cur.fetchone()
        if not repo:
            source_fk = repo[0]
        return render_template("bland_error.html")


        cur.execute("SELECT facility_pk FROM facilities WHERE fcode=%s;",(dest,))
        repo = cur.fetchone()
        if not repo:
            dest_fk = repo[0]
        return render_template("bland_error.html")


        cur.execute("SELECT user_pk FROM users WHERE username=%s;",(session["username"],))
        repo = cur.fetchone()
        if not repo:
            requester_fk = repo[0]
        return render_template("bland_error.html")




        cur.execute("SELECT f.fcode FROM assets AS a INNER JOIN asset_at AS aa ON a.asset_pk=aa.asset_fk INNER JOIN \
            facilities AS f ON f.facility_pk=aa.facility_fk WHERE aa.arrive_dt<= %s AND (aa.depart_dt> %s OR aa.depart_dt IS NULL) AND a.asset_tag=%s;", (request_dt, request_dt))
        repo = cur.fetchone()
        if not repo:
            if source != repo[0]:
                conn.commit()
                cur.close()
                conn.close()
                return render_template("bland_error.html")
            elif dest == repo[0]:
                conn.commit()
                return render_template("bland_error.html")
        else:
            return render_template("bland_error.html")

        cur.execute("INSERT INTO transfer_requests (requester_fk, request_dt, source_fk, dest_fk, asset_fk) VALUES (%s, %s, %s, %s, %s);",  (requester_fk, request_dt, source_fk, dest_fk, asset_fk))
        conn.commit()
        return render_template("sucessful_request.html")


    if request.method == 'GET':
        asset_list = []
        facility_list = []

        cur.execute('SELECT asset_tag FROM assets;')
        return_result = cur.fetchall()
        
        for items in return_result:
            row = dict()
            row['tag'] = items[0]
            asset_list.append(row)
        session['asset_list'] = asset_list

        cur.execute('SELECT fcode FROM facilities;')
        return_result = cur.fetchall()
    
        for items in return_result:
            row = dict()
            row['fcode'] = items[0]
            facility_list.append(row)

        session['facility_list'] = facility_list

        return render_template('transfer_request.html')






@app.route('/approve_req', methods = ['GET', 'POST'])
def approve_req():
    if not session['logged_in']:
            return redirect(url_for('login'))

    if session['role'] != 'Facilities Officer':
        return render_template('access_denied.html')
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()

    if request.method == 'GET' and 'req_id' in request.args:
        req_id = int(request.args['req_id'])
        
        #SQL
        cur.execute('SELECT a.asset_tag, f.facility_common_name, u.username, r.request_dt FROM transfer_requests AS r INNER JOIN \
            facilities AS f ON r.source_fk=f.facility_pk INNER JOIN users AS u ON r.requester_fk=u.user_pk INNER JOIN assets AS a ON \
            r.asset_fk=a.asset_pk WHERE r.request_pk=%s;', (req_id,))

        result = cur.fetchone()

        cur.execute('SELECT f.facility_common_name FROM transfer_requests AS r INNER JOIN \
            facilities AS f ON r.dest_fk=f.facility_pk WHERE r.request_pk=%s;', (req_id,))

        result_dest = cur.fetchone()
        

        #if request.method == 'GET' and 'asset' in request.args:
        if result == None or result_dest == None:
            conn.commit()
            return render_template('bland_error.html')
        else:
            session['request_report'] = []
            row = dict()
            row['tag'] = result[0]
            row['source'] = result[1]
            row['dest'] = result_dest[0]
            row['requester'] = result[2]
            row['request_dt'] = result[3]
            session['request_report'].append(row)
        conn.commit()
        return render_template('approve_req.html')




    elif request.method == 'POST':
        req_id = int(request.form['req_id'])
        approval = request.form['approval']
        if approval == 'False':
            cur.execute('DELETE FROM transfer_requests WHERE request_pk=%s;', (req_id,))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('dashboard'))

        else:
            user = session['username']
            approval_dt = str(datetime.now())
            cur.execute('UPDATE transfer_requests SET approval_dt=%s, approver_fk=(SELECT user_pk FROM users WHERE username=%s) WHERE request_pk=%s;', (approval_dt, user, req_id))
            cur.execute('INSERT INTO transfers (asset_fk, request_fk) VALUES ((SELECT asset_fk FROM transfer_requests WHERE request_pk=%s), %s);', (req_id, req_id))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('dashboard'))

    return render_template('generic_error.html')




@app.route('/update_transit', methods=['GET', 'POST'])
def update_transit():
    if not session['logged_in']:
        return redirect(url_for('login'))

    if session['role'] != 'Logistics Officer':
        return render_template('access_denied.html')


    if request.method == 'GET' and 'asset' in request.args:
        asset = int(request.args['asset'])
        SQL = "SELECT unload_dt from in_transit WHERE asset = '{}'".format(asset)
        cur.execute(SQL)
        res = cur.fetchall()
    else:   
        data = dict()
        data['asset'] = asset
        return render_template('update_transit.html', data = [data])
    
    if request.method == 'POST':
        asset = request.form['asset'] #a primary key identifier
        load = request.form['load_date']
        unload = request.form['unload_date']
        
        SQL = "UPDATE in_transit SET load_dt = %s, unload_dt = %s WHERE asset = '{}'".format(asset)
        data = (load, unload)
        cur.execute(SQL, data)
        SQL = "UPDATE asset_at SET arrive_dt = %s, depart_dt = %s WHERE asset_fk = '{}'".format(asset)
        data = (unload, load)
        cur.execute(SQL, data)
        conn.commit()
        return redirect(url_for('dashboard'))
    




# #EC??
@app.route('/transfer_report', methods = ['GET', 'POST'])
def transfer_report():
    # if not session['logged_in']:
    #     return redirect(url_for('login'))

    # conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    # cur = conn.cursor()

    # session['transfer_report'] = []

    

    # session['transfer_report'] = transfer_report

    return render_template('transfer_report.html')




if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)