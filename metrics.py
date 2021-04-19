import sensors
import time
import requests

while True:
	metrics = {}

	sensors.init()
	try:
		for chip in sensors.iter_detected_chips():
			if __debug__: 
				print(f'{chip} at {chip.adapter_name}')
			metrics[str(chip)] = {}
			for feature in chip:
				if __debug__: 
					print(f'{feature.label}: {feature.get_value():0.3f}')
				metrics[str(chip)][str(feature.label)] = feature.get_value()
	finally:
		sensors.cleanup()

	try:
		requests.post('http://localhost:5000/new', headers={"Date": str(time.time())}, json = metrics)
	except requests.exceptions.ConnectionError as e:
		print(e)
	time.sleep(10)
