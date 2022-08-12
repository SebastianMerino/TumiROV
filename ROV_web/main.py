from flask import Flask, render_template, Response, jsonify, request
from sonda import Sonda, calc_profundidad
from videostream import VideoStream
from puertosUSB import buscar_puerto
from propulsores import Propulsores
import logging
import cv2

# Iniciar sonda
idronaut = Sonda(buscar_puerto("AR0K3WI2A"))
idronaut.config()

# Iniciar propulsores
props = Propulsores(buscar_puerto("AR0K003IA"))

# Iniciar camaras
fuente1 = "rtsp://192.168.226.201:554"
fuente2 = "rtsp://192.168.226.203:554"
vs1 = VideoStream(fuente1).start()
vs2 = VideoStream(fuente2).start()

# Frame generator for video
def generate(vs):
    while True:
        (grabbed, frame) = vs.read()
        if not grabbed:
            continue
        frame = cv2.resize(frame,(352,286))
        # encode the frame in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        # ensure the frame was successfully encoded
        if not flag:
            continue
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

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
    dict['depth'] = calc_profundidad(p,lat=12.5)
    return jsonify(dict)

@app.route("/cam1")
def video_feed1():
    # return the response with the specific media type (mime type)
    return Response(generate(vs1),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/cam2")
def video_feed2():
    # return the response with the specific media type (mime type)
    return Response(generate(vs2),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/navegacion")
def navegacion():
    return render_template("navegacion.html")

@app.route('/prop_verticales')
def prop_verticales():
	return jsonify({'vel_izq':props.propIzq.vel,
		'vel_der':props.propDer.vel})

@app.post('/gamepad')
def gamepad():
	""" Esta función se llama cada vez que se actualiza info
	del gamepad """
	gp = request.json
	RVax = gp['axes']['RV']
	if RVax > 0.1 or RVax < -0.1: 
		props.set_vel_vertical(RVax)
	else:
		props.set_vel_vertical(0)
	return jsonify(gp)

if __name__ == '__main__':
    ip = "0.0.0.0"	# Poner 0.0.0.0 para que este abierto a cualquier direccion
    p = 8000			# Puerto

    # start the flask app
    app.run(host=ip, port=p, debug=False, threaded=True, use_reloader=False)
    
    vs1.stop()
    vs2.stop()
    
    idronaut.stop()
    idronaut.shutdown()