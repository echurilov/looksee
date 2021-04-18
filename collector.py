from flask import Flask, request
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
	