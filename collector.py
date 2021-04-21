from flask import Flask, request, jsonify
import sqlite3
import time

con = sqlite3.connect("metrics.db")
cursor = con.cursor()
cursor.execute(f"insert into metrics values ('start', 'start', {time.time()}, 0)")
con.commit()
con.close()

app = Flask(__name__)
@app.route("/")
def index():
	con = sqlite3.connect("metrics.db")
	cursor = con.cursor()
	output = ""
	for row in cursor.execute(f"SELECT * FROM metrics ORDER BY received ASC"):
		output += str(row) + "\n"
	con.close()
	return output

@app.route("/new", methods=['POST'])
def create():
	received = request.date or time.time()
	con = sqlite3.connect("metrics.db")
	cursor = con.cursor()
	metrics = request.get_json()
	for chip in metrics.keys():
		for label in metrics[chip].keys():
			cursor.execute(f"INSERT INTO metrics VALUES (?, ?, ?, ?)",(label, chip, received, metrics[chip][label]))
	con.commit()
	con.close()
	return ("",200)

@app.route("/show", methods=['GET'])
def show():
	con = sqlite3.connect("metrics.db")
	cursor = con.cursor()
	response = []
	start = request.args.get("start", 0) 
	stop = request.args.get("stop", time.time())
	label = request.args.get("label", "%")
	chip = request.args.get("chip", "%")
	limit = int(request.args.get("limit", 10))
	page = (int(request.args.get("page", 1))-1)*limit
	for (label,chip,received,value) in cursor.execute(
		"""SELECT * FROM metrics 
		WHERE received >= ? 
		AND received <= ? 
		AND label LIKE ? 
		AND chip LIKE ?
		ORDER BY received DESC
		LIMIT ?, ?;""",
		(start, stop, label, chip, page, limit)):
		response.append({"label": label,"chip": chip,"received": received, "value": value})
	con.commit()
	con.close()
	res = jsonify(response)
	res.headers.add('Access-Control-Allow-Origin', '*')
	return res
