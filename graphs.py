from flask import Flask, request
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/graph", methods=['POST'])
def graph():
	data = request.get_json()
	print(data)
	fig, ax = plt.subplots()
	for name in data["series"]:
		ax.plot(
			[datum[0] for datum in data["series"][name]],
			[datum[1] for datum in data["series"][name]]
		)
	output = StringIO()
	fig.savefig(output,format="svg")
	output.seek(0)
	return output.getvalue()
