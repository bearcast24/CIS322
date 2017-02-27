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
        cur.execute("SELECT username,password FROM user_accounts WHERE username = '{}' and password = '{}';".format(uname, pwd))
        #If user is found:
        if cur.fetchone() is not None:
            session['username'] = uname
            return render_template('dashboard.html')
        #If no user is found:
        return render_template('no_user.html')

    return render_template('login.html')   


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')




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
        cur.execute("SELECT asset_tag from assets WHERE asset_tag = '{}'".format(asset_tag))
        asset_there = cur.fetchone()[0]

        if not asset_there:
            cur.execute("INSERT INTO assets (asset_tag, description) VALUES ('{}', '{}') RETURNING asset_pk;".format(asset_tag, desc))
            conn.commit()
            asset_pk = cur.fetchone()[0]

            #Find asset home:
            cur.execute("SELECT facility_pk FROM facilities WHERE common_name='{}';".format(fac))
            facility_pk = cur.fetchone()[0]

            #Give asset the home it disserves:
            cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES ({}, {}, {});".format(asset_pk,facility_pk,arrive_dt)
            conn.commit()
            return redirect(url_for('add_asset'))
        #Chance are it is a spelling or case issue:   
        else:        
            return render_template('error_duplicate.html')



# #Access might be broken: Something janky is happening:
# @app.route('/dispose_asset', methods=['GET', 'POST'])
# def dispose_asset():
#     #Connect to postgres:
#     conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
#     cur  = conn.cursor()
#     #Check if user is permited:
#     cur.execute("SELECT role_name from user_accounts JOIN roles ON user_accounts.role_fk = roles.role_pk WHERE username = '{}';".format(session['username']))

#     job_role = cur.fetchone()[0]
#     if job_role != 'logistics officer':
#         return render_template('access_denied.html')

#     #Page fun:
#     if request.method == 'GET':
#         return render_template('dispose_asset.html')
#     #Req page:
#     if request.method == 'POST':
#         ass_tag = request.form['asset_tag']
#         cur.execute("SELECT asset_tag, disposed from assets WHERE asset_tag LIKE '{}';".format(ass_tag))







# # @app.route('/asset_report', methods=['GET', 'POST'])
# # def asset_report():












if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)