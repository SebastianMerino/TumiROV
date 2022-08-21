from flask import Flask, render_template, json
from vehicle import Vehicle

app = Flask(__name__)
PX4 = Vehicle("COM4")

@app.route("/")
def ROV():
	return render_template("ROV_1cam.html")

@app.route("/navegacion")
def navegacion():
    return render_template("navegacion.html")

@app.route("/datos_PX4")
def datos_px4():
	att_dict = dict(zip(['roll','pitch','yaw'],PX4.attitude))
	v_dict = dict(zip(['vx','vy','vz'],PX4.velocity))
	datos_dict = {'attitude':att_dict, 'velocity':v_dict,
		'time_boot':PX4.time_boot, 'motors': PX4.motors}
	return json.dumps(datos_dict)

if __name__ == '__main__':
	ip = "127.0.0.1"
	p = 8000			# Puerto

	PX4.start_data_rx()

	# start the flask app
	app.run(host=ip, port=p, debug=False, threaded=True, use_reloader=False)

PX4.stop_data_rx()