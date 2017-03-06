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
        cur.execute("SELECT username, password, role_name FROM user_accounts INNER JOIN roles ON role_pk = role_fk \
            WHERE username = '{}' and password = '{}';".format(uname, pwd))

        result = cur.fetchone()
        #If user is found:
        if result is not None:
            session['username'] = uname
            session['logged_in'] = True
            session['role'] = result[2]
            #send to Dashboard after getting signed in
            return redirect(url_for('dashboard.html'))
        #If no user is found:
        return render_template('no_user.html')


    return render_template('login.html')   


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if not session['logged_in']:
        #test for logged in session and redirect
        return redirect(url_for('login'))

    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
    tasks = []
    #Hard code for ease-> should use database to make avail forms

    #Logistics
    if session['role'] == "Logistics Officer":
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
    if session['role'] == "Facilities Officer":
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

    #Save asset changes
    conn.commit()
    cur.close()
    conn.close()
    return render_template('dashboard.html');









@app.route('/logout')
def logout():
    session['logged_in'] = False #Terminate the session
    #logout_user()
    session.clear()
    return redirect(url_for('login'))





@app.route('/create_user', methods=['GET', 'POST'])
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

#New pages:

@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
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
        cur.execute("SELECT fcode, common_name from facilities WHERE fcode = '{}' AND common_name = '{}';".format(fcode, common_name))
        res_fac = cur.fetchall()
        #add new
        if not res_fac: 
            cur.execute("INSERT INTO facilities (common_name, fcode) VALUES ('{}','{}');".format(fcode, common_name))
            conn.commit()
            return redirect(url_for('add_facility'))
        else: 
            return render_template('error_duplicate.html')


@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    #Connect to postgres:
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
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

    if request.method == 'GET':
        return render_template('add_asset.html')

    if request.method == 'POST':
        asset_tag = request.form['asset_tag']
        desc = request.form['description']
        fac = request.form['common_name']
        arrive_dt = request.form['date']

        #DB check:
        cur.execute("SELECT asset_tag from assets WHERE asset_tag = '{}';".format(asset_tag))
        asset_there = cur.fetchone()[0]

        if not asset_there:
            cur.execute("INSERT INTO assets (asset_tag, description) VALUES ('{}', '{}') RETURNING asset_pk;".format(asset_tag, desc))
            conn.commit()
            asset_pk = cur.fetchone()[0]

            #Find asset home:
            cur.execute("SELECT facility_pk FROM facilities WHERE common_name='{}';".format(fac))
            facility_pk = cur.fetchone()[0]

            #Give asset the home it disserves:
            cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES ({}, {}, {});".format(asset_pk,facility_pk,arrive_dt))
            conn.commit()
            return redirect(url_for('add_asset'))
        #Chance are it is a spelling or case issue:   
        else:        
            return render_template('error_duplicate.html')



# #Access might be broken: Something janky is happening:
# @app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
    #Connect to postgres:
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
    #Check if user is permited:
    cur.execute("SELECT role_name from user_accounts \
        JOIN roles ON user_accounts.role_fk = roles.role_pk WHERE username = '{}';".format(session['username']))

    job_role = cur.fetchone()[0]
    if job_role != 'logistics officer':
        return render_template('access_denied.html')

    #Page fun:
    if request.method == 'GET':
        return render_template('dispose_asset.html')
    #Req page:
    if request.method == 'POST':
        ass_tag = request.form['asset_tag']
        cur.execute("SELECT asset_tag, disposed from assets WHERE asset_tag LIKE '{}';".format(ass_tag))
        ret_assets = cur.fetchall()

        #item not there:
        if not ret_assets:
            return render_template('error_removed.html')
        #Remove item: (Need to add in way to see item alreeady removed)
        else: 
            cur.execute("UPDATE assets SET disposed = TRUE where asset_tag = '{}';".format(ass_tag))
            conn.commit()
            return render_template('dashboard.html')



@app.route('/asset_report', methods=['GET', 'POST'])
def asset_report():
    if request.method == 'GET':
        return render_template('asset_report.html')
    if request.method =='POST':
        time = request.form['date']
        fac = request.format['common_name']
    cur.execute("SELECT asset_tag, description, common_name, arrive_dt FROM assets \
        JOIN asset_at ON assets.asset_pk = asset_at.asset_fk \
        JOIN facilities ON asset_at.facility_fk = facilities.facility_pk \
        WHERE arrive_dt = '{}';".format(time))

    repo = cur.fetchall()

    asset_results = []
    for line in repo:
        data = dict()
        #line[0] = key
        data['asset_tag'] = line[0]
        data['description'] = line[1]
        data['common_name'] = line[2]
        data['arrive_dt'] = line[3]
        asset_results.append(data)
    session['asset_list'] = asset_results

    return redirect(url_for('asset_report'))









if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)