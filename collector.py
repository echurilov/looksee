from flask import Flask
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
