# import the necessary packages
from videostream import VideoStream
from flask import Response, Flask, render_template
import threading
import argparse
import cv2

outputFrame = None
lock = threading.Lock()		# avoid racing conditions
app = Flask(__name__)		# initialize a flask object

# initialize the video stream
# fuente = "rtsp://192.168.226.201:554"
fuente = 0
vs = VideoStream(fuente).start()

def sendFrame():
	global vs, outputFrame, lock
	while True:
		# read the next frame from the video stream, resize it
		frame = vs.read()
		if frame is None:
			continue

		frame = cv2.resize(frame,(352,286))
		with lock:
			outputFrame = frame.copy()

def generate():
	global outputFrame, lock
	# loop over frames from the output stream
	while True:
		with lock:
			if outputFrame is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
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

@app.route("/video_feed")
def video_feed():
	# return the response with the specific media type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device. Set to 0.0.0.0 to set the server available to anyone on the local network")
	ap.add_argument("-p", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	args = vars(ap.parse_args())

	tSend = threading.Thread(target=sendFrame)
	tSend.daemon = True
	tSend.start()
	
	# start the flask app
	app.run(host=args["ip"], port=args["port"], debug=False,
		threaded=True, use_reloader=False)

# release the video stream pointer
#vs.release()
vs.stop()