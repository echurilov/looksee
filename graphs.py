from flask import Flask, request, Response
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

@app.route("/graph", methods=['GET'])
def graph():
	fig, ax = plt.subplots(figsize=(11,6))
	for name in request.args:
		if not request.args[name]:
			continue
		line = request.args[name].split(';')
		points = [point.split(',') for point in line]
		ax.plot(
			np.array([point[0] for point in points],dtype=np.datetime64),
			np.array([point[1] for point in points],dtype=np.float32),
			label = name
		)
	fig.autofmt_xdate()
	ax.set_xlabel('Time')
	ax.set_title('Data')
	ax.legend(bbox_to_anchor = (1.01, .6))
	ax.grid(True)
	plt.tight_layout()
	output = StringIO()
	fig.savefig(output,format="svg")
	output.seek(0)
	return Response(output.getvalue(), mimetype = "image/svg+xml")
