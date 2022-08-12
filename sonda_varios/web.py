from math import sin
from flask import Flask, render_template, jsonify
from sonda import Sonda, calc_profundidad
from puertosUSB import buscar_puerto

hwid = '0403:6001'
idronaut = Sonda(buscar_puerto(hwid))
idronaut.config()
app = Flask(__name__)

@app.route("/")
def ROV():
    return render_template("ROV.html")

@app.route("/datos_sonda")
def datos_sonda():
    dict = idronaut.data_dict
    p = dict['press']
    dict['depth'] = calc_profundidad(p,lat=12.5)
    return jsonify(dict)

if __name__ == '__main__':
    idronaut.start()
    app.run(host='127.0.0.1', port=8000, debug=False, threaded=True, use_reloader=False)

idronaut.stop()
idronaut.shutdown()