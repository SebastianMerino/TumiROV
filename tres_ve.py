import cv2

fuente1 = "rtsp://admin:123456@192.168.226.201:554"
fuente2 = "rtsp://admin:123456@192.168.226.202:554"
fuente3 = "rtsp://admin:123456@192.168.226.203:554"

rov_cam1 = cv2.VideoCapture(fuente1)
rov_cam2 = cv2.VideoCapture(fuente2)
rov_cam3 = cv2.VideoCapture(fuente3)

while(rov_cam1.isOpened() & rov_cam2.isOpened() & rov_cam3.isOpened()):
    ret1,img1 = rov_cam1.read()
    ret2,img2 = rov_cam2.read()
    ret3,img3 = rov_cam3.read()

    if ret1 == True:
        cv2.imshow('rov_vid1',img1)
        if (cv2.waitKey(1) & 0xFF) == ord('s'):
            break
    if ret2 == True:
        cv2.imshow('rov_vid2',img2)

    if ret3 == True:
        cv2.imshow('rov_vid3',img3)

rov_cam1.release()
rov_cam2.release()
rov_cam3.release()
cv2.destroyAllWindows()
