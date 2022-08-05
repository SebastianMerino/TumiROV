from flask import Flask, render_template, jsonify
from sonda import Sonda
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
    g,c1,c2,c3,c4 = 9.78255, 9.72659, -2.2512E-5, 2.279E-10, -1.82E-15
    dict['depth'] = (c1*p + c2*p**2 + c3*p**3 + c4*p**4)/(g + 1.092E-6*p)
    return jsonify(dict)

if __name__ == '__main__':
    idronaut.start()
    app.run(host='127.0.0.1', port=8000, debug=False, threaded=True, use_reloader=False)

idronaut.stop()
idronaut.shutdown()