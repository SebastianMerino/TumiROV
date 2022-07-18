import cv2
from threading import Thread
from imutils.video import FPS
from imutils.video import VideoStream
import time

fuente = 0
rov_cam = cv2.VideoCapture(fuente)
#rov_cam = VideoStream(fuente).start()
fps = FPS().start()

def grabFrame():
    global rov_cam
    while rov_cam.isOpened():
        rov_cam.grab()

Tgrab = Thread(target=grabFrame)
Tgrab.daemon = True
Tgrab.start()

while rov_cam.isOpened():
    ret,img = rov_cam.retrieve()
    if ret == True:
        fps.update()
        cv2.imshow('rov_vid',img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
fps.stop()

"""
while True:
    img = rov_cam.read()
    if img is not None:
        fps.update()
        cv2.imshow('rov_vid',img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
fps.stop()
"""
rov_cam.release()
#rov_cam.stop()
cv2.destroyAllWindows()

print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
