from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
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
		return redirect(url_for('login.html'))
	elif request.method == 'POST':
		return render_template('Login.html')





@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')





if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)