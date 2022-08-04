from flask import Flask, render_template, jsonify
from sonda import Sonda

idronaut = Sonda('COM5')
idronaut.config()
app = Flask(__name__)

@app.route("/")
def ROV():
    return render_template("ROV.html")

@app.route("/datos_sonda")
def datos_sonda():
    return jsonify(idronaut.data_dict)

if __name__ == '__main__':
    idronaut.start()
    app.run(host='127.0.0.1', port=8000, debug=False, threaded=True, use_reloader=False)

idronaut.stop()
idronaut.shutdown()