from flask import Flask, render_template, Response
from sonda import Sonda
from videostream import VideoStream
import serial
import cv2

app = Flask(__name__)

puertoSonda = input('Ingrese puerto de la sonda: ')
puertoProp = input('Ingrese puerto de los propulsores: ')

# idronaut = Sonda('/dev/ttyUSB'+puertoSonda)
# idronaut.config()

# -------------------------  PROPULSORES  ---------------------------
prop = serial.Serial(port = '/dev/ttyUSB'+puertoProp, baudrate=115200)
def cambiar_velocidad_propulsores(RPM):
    prop1CW = 0x6141000097
    prop1CCW = 0x6142000097
    prop2CW = 0x6241000098
    prop2CCW = 0x6242000098
    if RPM == 0:
        command1 = prop1CCW | (RPM << 8)
        command2 = prop2CCW | (RPM << 8)
        prop.write(command1.to_bytes(5,'big'))
        prop.write(command2.to_bytes(5,'big'))
        command1 = prop1CW | (RPM << 8)
        command2 = prop2CW | (RPM << 8)
        prop.write(command1.to_bytes(5,'big'))
        prop.write(command2.to_bytes(5,'big'))
    else:
        if RPM > 0:
            command1 = prop1CCW | (RPM << 8)
            command2 = prop2CCW | (RPM << 8)
        else:
            RPM = -RPM
            command1 = prop1CW | (RPM << 8)
            command2 = prop2CW | (RPM << 8)
        prop.write(command1.to_bytes(5,'big'))
        prop.write(command2.to_bytes(5,'big'))

def subir():
    command1 = 0x6142138897
    command2 = 0x6241138898
    prop.write(command1.to_bytes(5,'big'))
    prop.write(command2.to_bytes(5,'big'))
    print(hex(command1))
    print(hex(command2))

def sumergirse():
    command1 = 0x6141138897
    command2 = 0x6242138898
    prop.write(command1.to_bytes(5,'big'))
    prop.write(command2.to_bytes(5,'big'))
    print(hex(command1))
    print(hex(command2))

def subir_mas():
    command1 = 0x614203E897
    command2 = 0x624103E898
    prop.write(command1.to_bytes(5,'big'))
    prop.write(command2.to_bytes(5,'big'))
    print(hex(command1))
    print(hex(command2))

def sumergirse_mas():
    command1 = 0x614103E897
    command2 = 0x624203E898
    prop.write(command1.to_bytes(5,'big'))
    prop.write(command2.to_bytes(5,'big'))
    print(hex(command1))
    print(hex(command2))

def parar():
    prop1CW = 0x6141000097
    prop1CCW = 0x6142000097
    prop2CW = 0x6241000098
    prop2CCW = 0x6242000098
    prop.write(prop1CW.to_bytes(5,'big'))
    prop.write(prop1CCW.to_bytes(5,'big'))
    prop.write(prop2CW.to_bytes(5,'big'))
    prop.write(prop2CCW.to_bytes(5,'big'))
# ------------------------------------------------------------------

# idronaut.start()

# Iniciar el stream
fuente1 = "rtsp://192.168.226.201:554"
fuente2 = "rtsp://192.168.226.203:554"
vs1 = VideoStream(fuente1).start()
vs2 = VideoStream(fuente2).start()

# loop over frames from the video stream
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

@app.route("/")
def ROV():
    return render_template("ROV.html")

@app.route("/datos_sonda")
def datos_sonda():
    # return idronaut.data_json
    return None

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

# -------------------------  PROPULSORES  ---------------------------
@app.route("/navegacion")
def navegacion():
    return render_template("navegacion.html")

# @app.route('/prop_<cmd>')
# def command(cmd=None):
#     global prop_RPM
#     if cmd == "reset":
#        prop_RPM = 0
#     elif cmd == "acelerar":
#         prop_RPM += 10
#     elif cmd == "desacelerar":
#         prop_RPM -= 10
#     elif cmd == "subir":
#         prop_RPM += 500
#     elif cmd == "bajar":
#         prop_RPM -= 500
    
#     if prop_RPM >= 5000: prop_RPM = 5000 
#     if prop_RPM <= -5000: prop_RPM = -5000

#     cambiar_velocidad_propulsores(prop_RPM)
#     response = "Comando: {}".format(cmd)
#     return response, 200, {'Content-Type': 'text/plain'}

@app.route('/prop_<cmd>')
def command(cmd=None):
    if cmd == "reset":
       parar()
    elif cmd == "acelerar":
        subir()
    elif cmd == "desacelerar":
        sumergirse
    elif cmd == "subir":
        subir_mas()
    elif cmd == "bajar":
        sumergirse_mas()
    return 'xd'
# -----------------------------------------------------------------

if __name__ == '__main__':
    ip = "0.0.0.0"	# Poner 0.0.0.0 para que este abierto a cualquier direccion
    p = 8000			# Puerto

    # start the flask app
    app.run(host=ip, port=p, debug=False, threaded=True, use_reloader=False)
    
    vs1.stop()
    vs2.stop()
    # idronaut.stop()
    # idronaut.shutdown()