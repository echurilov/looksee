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
		output = output + str(row) + "\n"
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
	for row in cursor.execute(
		"""SELECT * FROM metrics 
		WHERE received >= ? 
		AND received <= ? 
		AND label LIKE ? 
		AND chip LIKE ? 
		ORDER BY received ASC""",
		(start, stop, label, chip)):
		response.append({"label": row[0],"chip": row[1],"received": row[2], "value": row[3]})
	con.commit()
	con.close()
	return jsonify(response)
	