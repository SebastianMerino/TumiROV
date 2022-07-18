from flask import Flask, render_template, request
from sonda import Sonda

idronaut = Sonda()
#idronaut.config()
idronaut.start()
app = Flask(__name__)

@app.route("/")
def ROV():
    return render_template("ROV.html")

@app.route("/datos_sonda")
def datos_sonda():
    return idronaut.data_json

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False, threaded=True, use_reloader=False)

idronaut.stop()