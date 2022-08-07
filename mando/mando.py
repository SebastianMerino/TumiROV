from flask import Flask, render_template, jsonify, request
from propulsores import Propulsores
import logging

prop = Propulsores('/dev/ttyUSB0')

# Empezar app de Flask sin log
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route("/")
def ROV():
	return render_template("ROV.html")

@app.route("/navegacion")
def navegacion():
	return render_template("navegacion.html")

@app.route('/prop_verticales')
def prop_verticales():
	return jsonify({'rpm':prop.rpm})

@app.post('/gamepad')
def gamepad():
	""" Esta función se llama cada vez que se actualiza info
	del gamepad """
	gp = request.json
	prop.set_vel_vertical(gp['axes']['RV'])
	return jsonify(gp)

if __name__ == '__main__':
	ip = "127.0.0.1"
	p = 8000			# Puerto

	# start the flask app
	app.run(host=ip, port=p, debug=False, threaded=True, use_reloader=False)