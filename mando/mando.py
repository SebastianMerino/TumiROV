from flask import Flask, render_template, jsonify
from propulsores import Propulsores

prop = Propulsores('/dev/ttyUSB0')
app = Flask(__name__)

propRPM = 0

@app.route("/")
def ROV():
	return render_template("ROV.html")

@app.route("/navegacion")
def navegacion():
    return render_template("navegacion.html")

@app.route('/prop_<cmd>')
def command(cmd=None):
    """ Manda un comando segun lo que se presione """
    global propRPM
    if cmd == "reset":
        propRPM = 0
    elif cmd == "acelerar":
        propRPM += 100
        if propRPM >= 5000: propRPM = 5000
    elif cmd == "desacelerar":
        propRPM -= 100
        if propRPM <= -5000: propRPM = -5000
    elif cmd == "subir":
        propRPM = 100
    elif cmd == "bajar":
        propRPM = -100
    prop.set_speed_ROV(propRPM)
    return jsonify({'RPM':propRPM})

if __name__ == '__main__':
	ip = "127.0.0.1"
	p = 8000			# Puerto

	# start the flask app
	app.run(host=ip, port=p, debug=False, threaded=True, use_reloader=False)