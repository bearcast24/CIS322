from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
import json
#This should pull all configuations from the json file:
from config import dbname, dbhost, dbport, lost_priv, lost_pub, user_pub, prod_pub


app = Flask(__name__)

#Enter and Exit LOST
@app.route('/', methods= ['GET', 'POST'])
def login():
	if request.method == 'POST': #Need to store login state??
		return redirect(url_for('Report_filter'))
	else: #Ie not a good login
		return render_template('Login.html')

@app.route('/logout')
def logout():
	#Need to change the state of being logged in once we issue logins 
	return render_template('Logout.html')


#Request report:
@app.route('/Report_filter', methods=['GET', 'POST'])
def Report_filter():
	if request.method == 'POST':
		session["filter_date"] = request.form["search_date"]
		session["facilities"] = request.form["search_fac"]
		#Use a dictionary in recode for growth
		if request.form['report_type'] == 'Facilities':
			return redirect(url_for('Facility_inventory'))

		elif request.form['report_type'] == 'Transit':
			return redirect(url_for('In_Transit'))

	return render_template('Report_filter.html')



#Report runs:
@app.route('/Facility_inventory')
def Facility_inventory():
	conn = psycopg2.connect(dbname=dbname, port=dbport, host=dbhost)
	cur = conn.cursor()

	cur.execute("SELECT facilities.common_name, assets.asset_tag, assets.description, asset_at.arrive_dt, asset_at.depart_dt FROM \
		facilities INNER JOIN asset_at ON facilities.facility_pk=asset_at.facility_fk INNER JOIN assets ON asset_at.asset_fk=assets.asset_pk \
		WHERE facilities.fcode={0} AND asset_at.arrive_dt<={1} AND asset_at.depart_dt>={1};".format(session["search_fac"],session["search_date"]))
	
	report = cur.fetchall()
	facility_report = []

	for line in report:
		row = dict()
		row["common_name"] = line[0]
		row["asset_tag"] = line[1]
		row["description"] = line[2]
		row["arrive_dt"] = line[3]
		row["depart_dt"] = line[4]

		facility_report.append(row)

	session["facility_report"] = facility_report
	return render_template('Facility_Inventory.html')


@app.route('/In_Transit')
def In_Transit():
	conn = psycopg2.connect(dbname=dbname, port=dbport, host=dbhost)
	cur = conn.cursor()

	cur.execute("SELECT facilities.common_name, assets.asset_tag, assets.description, asset_on.load_dt, asset_on.unload_dt, convoys.request \
	FROM asset_on INNER JOIN convoys ON asset_on.convoy_fk=convoys.convoy_pk INNER JOIN assets ON asset_on.asset_fk=assets.asset_pk \
	INNER JOIN facilities ON convoys.source_fk=facilities.facility_pk \
	WHERE asset_on.load_dt<={0} AND asset_on.unload_dt>={0};".format(session["search_date"]))

	report = cur.fetchall()
	transit_report = []

	for line in report:
		row = dict()
		cur.execute("SELECT facilities.common_name FROM facilities INNER JOIN convoys ON convoys.dest_fk=facilities.facility_pk \
			WHERE convoys.request={0};", (line[5])) #From piazaa
		dest = cur.fetchone()
		row["source"] = line[0]
		row["destination"] = dest[0]
		row["asset_tag"] = line[1]
		row["description"] = line[2]
		row["load_dt"] = line[3]
		row["unload_dt"] = line[4]
		
		transit_report.append(row)

	session["In_Transit"] = transit_report
	return render_template('In_Transit.html')

#Rest stuffs:

@app.route('/rest')
def rest():
	return render_template('rest.html')

@app.route('/rest/lost_key',  methods=['POST'])
def lost_key():
	result = dict()
    result['timestamp'] = datetime.datetime.utcnow().isoformat()
    result['result'] = 'OK'
    result[key] = 'random_key' #using test key instead of random gernation
    final_data = json.dumps(result)
    
    return final_data



@app.route('/rest/activate_user', methods=['POST'])
def activate_user():
	if request.method == 'POST':
		requests = json.loads(request.form['arguments'])

		dat = dict()
		dat["timestamp"] = req["timestamp"]

		#SQL FUNS:
		conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
		cur = conn.cursor()
		cur.execute("SELECT user_pk, active FROM users WHERE username={};".format(requests["username"]))
		#Catch the output from the sql call  (W3 SQL help)
		output = cur.fetchone()
		
		if ouptut == None:
			dat["result"] = "NEW"
			cur.execute("INSERT INTO users (username, active) VALUES ({}, TRUE)".format(requests["username"]))
		#else all else fails	
		dat["result"] = "FAIL"

		final_data = json.dumps(dat)

		return final_data



@app.route('/rest/suspend_user')
def suspend_user():
	if request.method = "POST" and "arguments" in request.form:
		req = json.loads(request.form["arguments"])
		dat = dict()
		dat["timestamp"] = req["timestamp"]
		dat["result"] = "OK"

		conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
		cur = conn.cursor()
		cur.execute("SELECT user_pk, active FROM users WHERE username={}", (req["username"],))

		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = False

		if result != False:
			cur.execute("UPDATE users SET active=FALSE WHERE username={}", (req["username"],))

		data = json.dumps(dat)
		return data



@app.route('/rest/list_products')
def list_products():
	if request.method = "POST" and "arguments" in request.form:
		req = json.loads(request.form["arguments"])
		dat = dict()
		dat["timestamp"] = req["timestamp"]
		##Told to steal code directly from Dan's implementation, so that's exactly what I'm going to do
		dat["result"] = "OK"
		data = json.dumps(dat)
		return data



@app.route('/rest/add_products')
def add_products():
	if request.method = "POST" and "arguments" in request.form:
		req = json.loads(request.form["arguments"])
		dat = dict()
		dat["timestamp"] = req["timestamp"]
		##TODO
		dat["result"] = "OK"
		data = json.dumps(dat)
		return data



@app.route('/rest/add_asset')
def add_asset():
	if request.method = "POST" and "arguments" in request.form:
		req = json.loads(request.form["arguments"])
		dat = dict()
		dat["timestamp"] = req["timestamp"]
		##TODO
		dat["result"] = "OK"
		data = json.dumps(dat)
		return data








if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)