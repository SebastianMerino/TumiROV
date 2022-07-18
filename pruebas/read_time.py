import cv2
from threading import Thread
from imutils.video import FPS
from imutils.video import VideoStream
import time

fuente = 0
rov_cam = cv2.VideoCapture(fuente)
rov_cam.read()

total_grab = 0
total_ret = 0
i = 0
while rov_cam.isOpened():
    start = time.time()
    rov_cam.grab()
    total_grab += time.time() - start

    start = time.time()
    (ret,img) = rov_cam.retrieve()
    total_ret += time.time() - start
    if img is not None:
        cv2.imshow('rov_vid',img)
        i += 1
        if cv2.waitKey(1) & 0xFF == 27:
            break

rov_cam.release()
print('Mean grab time:',total_grab/i*1E3, 'ms')
print('Mean retrieve time: ',total_ret/i*1E3, 'ms')
cv2.destroyAllWindows()

