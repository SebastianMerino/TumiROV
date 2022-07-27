from videostream import VideoStream
from flask import Response, Flask, render_template
import cv2

app = Flask(__name__)		# initialize a flask object

# Iniciar el stream
fuente = 0		# "rtsp://192.168.226.201:554"
vs1 = VideoStream(fuente).start()

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
def index():
	# return the rendered template
	return render_template("ROV_1cam.html")

@app.route("/cam1")
def video_feed():
	# return the response with the specific media type (mime type)
	return Response(generate(vs1),
		mimetype = "multipart/x-mixed-replace; boundary=frame")


# Main thread of execution
if __name__ == '__main__':
	ip = "127.0.0.1"	# Poner 0.0.0.0 para que este abierto a cualquier direccion
	p = 8000			# Puerto

	# start the flask app
	app.run(host=ip, port=p, debug=False, threaded=True, use_reloader=False)

	# release the video stream pointer
	vs1.stop()