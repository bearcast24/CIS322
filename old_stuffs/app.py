from flask import Flask, render_template, request
from config import dbname, dbhost, dbport

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Login.html')

@app.route('/welcome')
def welcome():
    return render_template('Login.html')

@app.route('/logout')
def logout():
    return render_template('Logout.html')



@app.route('/Report')
def Report():
    return render_template('Report_filter.html')



@app.route('/In_transit')
def Transit():
    return render_template('In_Transit.html')

@app.route('/Facility_inventory ')
def Facility():
    return render_template('Facility_inventory.html')









#Hapton????
res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
processed_data = []   # this is the processed result I'll stick in the session (or pass to the template)
for r in res:
    processed_data.append( dict(zip(('column_name1', 'column_name2'), r)) )  # just making a dict out of the tuples from res
session['processed_data_session_name'] = processed_data













