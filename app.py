from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('Login.html')

@app.route('/logout')
def goodbye():
    return render_template('Logout.html')
