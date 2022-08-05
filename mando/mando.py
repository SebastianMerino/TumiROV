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

# @app.route('/gamepad_<cmd>')
# def command(cmd=None):
#     """ Manda un comando segun el boton que se presione 
#     Leyenda flechas -> Left, Right, Up, Down
#     """
#     rpm_actual = prop.rpm
#     if cmd == "B":
#         rpm_actual = 0
#     elif cmd == "Y":
#         rpm_actual += 100
#         if rpm_actual >= 5000: rpm_actual = 5000
#     elif cmd == "A":
#         rpm_actual -= 100
#         if rpm_actual <= -5000: rpm_actual = -5000
#     elif cmd == "U":
#         rpm_actual = 1000
#     elif cmd == "D":
#         rpm_actual = -1000
#     prop.set_speed_ROV(rpm_actual)
#     return jsonify({'rpm':rpm_actual})

@app.route('/gamepad', methods=['POST','GET'])
def gamepad():
    axes = request.json['axes']
    prop.set_vel_vertical(axes['RV'])
    return jsonify(axes)

if __name__ == '__main__':
	ip = "127.0.0.1"
	p = 8000			# Puerto

	# start the flask app
	app.run(host=ip, port=p, debug=False, threaded=True, use_reloader=False)