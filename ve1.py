import cv2

# fuente = "rtsp://admin:123456@192.168.226.201:554"
fuente = "rtsp://192.168.226.202:554"
#framecount = 1
rov_cam = cv2.VideoCapture(fuente)
while(rov_cam.isOpened()):
    ret,img = rov_cam.read()
    if ret == True:
        cv2.imshow('rov_vid',img)
        #framecount += 1
        if cv2.waitKey(1) & 0xFF == 27:
            break
rov_cam.release()
cv2.destroyAllWindows()

#print(framecount)
