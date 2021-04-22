from flask import Flask, request, Response
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

@app.route("/graph", methods=['GET'])
def graph():
	fig, ax = plt.subplots()
	for name in request.args:
		line = request.args[name].split(';')
		points = [point.split(',') for point in line]
		ax.plot(
			np.array([point[0] for point in points],dtype=np.datetime64),
			[point[1] for point in points]
		)
	ax.set_xlabel('Time')
	fig.autofmt_xdate()
	ax.set_title('Data')
	ax.grid(True)
	output = StringIO()
	fig.savefig(output,format="svg")
	output.seek(0)
	return Response(output.getvalue(), mimetype = "image/svg+xml")
