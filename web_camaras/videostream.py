"""
Librería para obtener los datos de las cámaras con threads para
mejorar el frame rate. Adaptado de librería imutils.video
https://github.com/PyImageSearch/imutils
"""
from threading import Thread
import cv2

class VideoStream:
	def __init__(self, src=0):
		""" Initializes the video camera stream and read the first frame """
		self.capture = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.capture.read()
		self.running = False		# Stop flag

	def start(self):
		""" Starts the thread to read frames from the video stream """
		self.running = True
		self.t = Thread(target=self.update, args=())
		self.t.daemon = True
		self.t.start()
		return self

	def update(self):
		""" Keeps looping infinitely until the thread is stopped """
		while self.running:
			(self.grabbed, self.frame) = self.capture.read()

	def read(self):
		""" Returns the frame most recently read """
		return self.grabbed, self.frame

	def stop(self):
		""" Indicates that the thread should be stopped """
		self.running = False
		self.capture.release()
