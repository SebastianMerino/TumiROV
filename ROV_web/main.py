from flask import Flask, Response, render_template, jsonify, request
from sonda import Sonda, calc_profundidad
from videostream import VideoStream
from propulsores import Propulsores
from puertosUSB import buscar_puerto
from jetson import JetsonPin
from vehicle import Vehicle
import cv2
import logging

# ------------------------- SENSORES -------------------------------
# Propulsores
props = Propulsores(buscar_puerto("AR0K003IA"))

# Sonda
idronaut = Sonda(buscar_puerto("AR0K3WI2A"))
idronaut.config()
idronaut.start()

# Pixhawk
puerto = buscar_puerto('MAVLink')
PX4 = Vehicle(puerto)
PX4.arm()
PX4.start_data_rx()

# Luces
luces = JetsonPin(11)

# Camaras
fuente1 = "rtsp://192.168.226.201:554"
fuente2 = "rtsp://192.168.226.203:554"
vs1 = VideoStream(fuente1).start()
vs2 = VideoStream(fuente2).start()
def generate(vs):
	""" Objeto generador de frames codificados """
	while True:
		(grabbed, frame) = vs.read()
		if not grabbed:
			continue
		frame = cv2.resize(frame,(352,286))
		# encode the frame in JPEG format
		(flag, encodedImage) = cv2.imencode(".jpg", frame)
		if not flag:
			continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')
# -----------------------------------------------------------------

# ---------------------- PÁGINA WEB -------------------------------
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route("/")
def ROV():
	return render_template("ROV.html")

@app.route("/datos_sonda")
def datos_sonda():
	dict = idronaut.data_dict
	p = dict['press']
	lat = 12.5      # Latitud en Pucusana
	dict['depth'] = calc_profundidad(p,lat)
	return jsonify(dict)

# Para las cámaras se devuelve las respuestas con el media type
@app.route("/cam1")
def video_feed1():
	return Response(generate(vs1),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/cam2")
def video_feed2():
	return Response(generate(vs2),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/navegacion")
def navegacion():
	return render_template("navegacion.html")

@app.route('/prop_verticales')
def prop_verticales():
	return jsonify({'vel_izq':props.propIzq.vel,
		'vel_der':props.propDer.vel})

@app.route("/datos_PX4")
def datos_px4():
	att_dict = dict(zip(['roll','pitch','yaw'],PX4.attitude))
	v_dict = dict(zip(['vx','vy','vz'],PX4.velocity))
	datos_dict = {'attitude':att_dict, 'velocity':v_dict,
		'time_boot':PX4.time_boot, 'motors': PX4.motors_vel}
	return jsonify(datos_dict)

presionado = False
@app.post('/gamepad')
def gamepad():
	""" Se ejecuta cada vez que se postea info del gamepad """
	gp = request.json
	global presionado

	# Propulsores verticales
	RVax = gp['axes']['RV']
	if RVax > 0.1 or RVax < -0.1: 
		props.set_vel_vertical(RVax)
	else:
		props.set_vel_vertical(0)

	# Propulsores horizontales
	RHax = gp['axes']['RH']
	if RHax > 0.1 or RHax < -0.1: 
		PX4.girar(RHax)
	else:
		PX4.girar(0)
	LVax = gp['axes']['LV']

	if LVax > 0.1 or LVax < -0.1: 
		PX4.avanzar(LVax)
	else:
		PX4.avanzar(0)
	LHax = gp['axes']['LH']

	if LHax > 0.1 or LHax < -0.1: 
		PX4.lateral(LHax)
	else:
		PX4.lateral(0)
		
	
	#Luces
	if gp['buttons']['R1'] and not presionado:
		presionado = True
		luces.switch()
	if not gp['buttons']['R1']:
		presionado = False

	return jsonify(gp)
# ----------------------------------------------------------------------------

# --------------------------------- MAIN -------------------------------------
if __name__ == '__main__':
	ip = "0.0.0.0"      # Para que este disponible desde cualquier IP en la red
	p = 8000			# Puerto

	# Correr la app hasta el ctrl+C
	app.run(host=ip, port=p, debug=False, threaded=True, use_reloader=False)
	
	# Apagar todo
	vs1.stop()
	vs2.stop()
	idronaut.stop()
	idronaut.shutdown()
	props.close()
	luces.close()
	PX4.stop_data_rx()
	PX4.disarm()
	PX4.close_conn()