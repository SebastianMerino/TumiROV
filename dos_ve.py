import cv2

fuente1 = "rtsp://192.168.226.201:554"
fuente2 = "rtsp://192.168.226.202:554"

rov_cam1 = cv2.VideoCapture(fuente1)
rov_cam2 = cv2.VideoCapture(fuente2)

while(rov_cam1.isOpened() & rov_cam2.isOpened()):
    rov_cam1.grab()
    rov_cam2.grab()

    ret1,img1 = rov_cam1.retrieve()
    ret2,img2 = rov_cam2.retrieve()

    if ret1 == True & ret2 == True:
        cv2.imshow('rov_vid1',img1)
        cv2.imshow('rov_vid2',img2)

    if (cv2.waitKey(1) & 0xFF) == 27:
        break

rov_cam1.release()
rov_cam2.release()
cv2.destroyAllWindows()
