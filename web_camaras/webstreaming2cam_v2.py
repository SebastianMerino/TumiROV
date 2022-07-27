from videostream import VideoStream
from flask import Response, Flask, render_template
import cv2

app = Flask(__name__)		# initialize a flask object

# initialize the video stream
fuente = "rtsp://192.168.226.201:554"
vs1 = VideoStream(fuente).start()

fuente2 = "rtsp://192.168.226.202:554"
vs2 = VideoStream(fuente2).start()

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
	return render_template("ROV_2cam.html")

@app.route("/cam1")
def video_feed1():
	# return the response generated with the media type (mime type)
	return Response(generate(vs1),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/cam2")
def video_feed2():
	# return the response generated with the media type (mime type)
	return Response(generate(vs2),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':
	ip = "0.0.0.0"	# Poner 0.0.0.0 para que este abierto a cualquier direccion
	p = 8000			# Puerto

	# start the flask app
	app.run(host=ip, port=p, debug=False, threaded=True, use_reloader=False)

	# stop stream threads
	vs1.stop()
	vs2.stop()