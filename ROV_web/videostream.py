from threading import Thread
import cv2

class VideoStream:
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		self.capture = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.capture.read()

		# initialize the thread name and stop flag
		self.running = False

	def start(self):
		# start the thread to read frames from the video stream
		self.running = True
		self.t = Thread(target=self.update, args=())
		self.t.daemon = True
		self.t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while self.running:
			(self.grabbed, self.frame) = self.capture.read()

	def read(self):
		# return the frame most recently read
		return self.grabbed, self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.running = False
		#self.t.join()
		self.capture.release()
