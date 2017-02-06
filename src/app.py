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


















