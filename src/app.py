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
@app.route('/', methods= ['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET': #Need to store login state??
        return render_template('login.html')

    elif request.method == 'POST':
        uname = request.form['username']        
        pwd = request.form['password']
        #Connect to postgres:
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        #queries:
        cur.execute("SELECT username,password FROM user_accounts WHERE username = '{}' and password = '{}'".format(uname, pwd))
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
        session['username'] = uname
        #Connect to postgres:
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        #queries:
        cur.execute("SELECT username, password FROM user_accounts where username = '{}' AND password = '{}'".format(uname, pwd))
        #logic:
        #user is in user table:
        if cur.fetchone() is not None:
            return render_template('user_exists.html')
        else: 
            cur.execute("INSERT INTO user_accounts(username,password) VALUES ('{}', '{}');"..format(uname, pwd))
            conn.commit()
            return render_template('user_added.html')


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)