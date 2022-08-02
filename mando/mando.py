from flask import Flask, render_template
import serial
import time

# Configuring serial connections
prop = serial.Serial(
    port = '/dev/ttyUSB1',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

def cambiar_velocidad_propulsores(RPM):
    prop1CW = 0x6141000097
    prop1CCW = 0x6142000097
    prop2CW = 0x6241000098
    prop2CCW = 0x6142000098
    if RPM >= 0:
        command1 = prop1CCW | (RPM << 8)
        command2 = prop2CCW | (RPM << 8)
    else:
        RPM = -RPM
        command1 = prop1CW | (RPM << 8)
        command2 = prop2CW | (RPM << 8)
    #prop.write(command1)
    #prop.write(command2)
    #print(hex(command1))
    #print(hex(command2))

app = Flask(__name__)

prop_RPM = 0

@app.route("/")
def ROV():
	return render_template("ROV.html")

@app.route("/navegacion")
def navegacion():
    return render_template("navegacion.html")

@app.route('/prop_<cmd>')
def command(cmd=None):
    global prop_RPM
    if cmd == "reset":
       prop_RPM = 0
    elif cmd == "acelerar":
        prop_RPM += 10
        if prop_RPM >= 5000: prop_RPM = 5000 
    elif cmd == "desacelerar":
        prop_RPM -= 10
        if prop_RPM <= -5000: prop_RPM = -5000
    elif cmd == "subir":
        while prop_RPM < 5000:
            prop_RPM += 10
            cambiar_velocidad_propulsores(prop_RPM)        
    elif cmd == "bajar":
        while prop_RPM > -5000:
            prop_RPM -= 10
            cambiar_velocidad_propulsores(prop_RPM)   
    cambiar_velocidad_propulsores(prop_RPM)
    response = "Moving {}".format(prop_RPM)
    return response, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
	ip = "127.0.0.1"
	p = 8000			# Puerto

	# start the flask app
	app.run(host=ip, port=p, debug=False, threaded=True, use_reloader=False)

