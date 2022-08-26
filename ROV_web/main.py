from flask import Flask, Response, render_template, jsonify, request
from sonda import Sonda, calc_profundidad
from videostream import VideoStream
from propulsores import *
from serial.tools.list_ports import grep
from jetson import JetsonPin
from vehicle import Vehicle
import cv2
import logging

# ------------------------- SENSORES -------------------------------
# Puertos USB
def buscar_puerto(name):
    return next(grep(name)).device

# Propulsores
props = Propulsores(buscar_puerto("AR0K003I"))
Propulsor.MAX_RPM = 5000
props.start_tx()

# Sonda
idronaut = Sonda(buscar_puerto("AR0K3WI2"))
idronaut.config()
idronaut.start()

# Pixhawk
PX4 = Vehicle(buscar_puerto('Pixhawk'))
PX4.MAX_PWM = 1350
PX4.arm()
PX4.start_rx()

# Luces
luces = JetsonPin(11)
print('Luces listas!')

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

# ---------------------- PAGINA WEB -------------------------------
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
	datos_dict = {'attitude':att_dict, 'velocity':v_dict, 'vel_mod':PX4.vel_mod,
		'time_boot':PX4.time_boot, 'motors': PX4.motors}
	print(datos_dict)
	return jsonify(datos_dict)

presionado = False
@app.post('/gamepad')
def gamepad():
	""" Se ejecuta cada vez que se postea info del gamepad """
	gp = request.json
	global presionado
	if gp['buttons']['U']:
		PX4.avanzar(1)
	elif gp['buttons']['D']:
		PX4.avanzar(-1)
	elif gp['buttons']['R']:
		PX4.lateral(1)
	elif gp['buttons']['L']:
		PX4.lateral(-1)
	elif gp['buttons']['B']:
		PX4.girar(1)
	elif gp['buttons']['X']:
		PX4.girar(-1)
	else:
		PX4.avanzar(0)
	
	if gp['buttons']['Y']:
		props.subir(1)
	elif gp['buttons']['A']:
		props.subir(-1)
	else:
		props.subir(0)
	
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
	props.stop_tx()
	props.close()
	luces.close()
	print('Luces apagadas!')
	PX4.stop_rx()
	PX4.disarm()
	PX4.close_conn()