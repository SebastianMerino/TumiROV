import socket, cv2, pickle, struct, time

fuente1 = "rtsp://192.168.226.201:554"
fuente2 = "rtsp://192.168.226.202:554"

def ReadSendFrame(cam,sock,cam_num):
	ret,frame = cam.retrieve()
	if ret == True:
		# Pack size of frame + frame
		frame = cv2.resize(frame,(235,192))	
		a = pickle.dumps(frame)
		message = struct.pack("Q",len(a))+cam_num+a
		sock.sendall(message)

host_ip = '192.168.226.100'
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(socket_address)	# Socket Bind
server_socket.listen(5) 			# Socket Listen
print("LISTENING AT:",socket_address)

# Socket Accept
client_socket,addr = server_socket.accept()
print('GOT CONNECTION FROM:',addr)
if client_socket:
	rov_cam1 = cv2.VideoCapture(fuente1)
	rov_cam2 = cv2.VideoCapture(fuente2)
	
	#start_time = time.time()
	while(rov_cam1.isOpened() & rov_cam2.isOpened()):
		rov_cam1.grab()
		rov_cam2.grab()
		#if (time.time() - start_time > 0.2):
		ReadSendFrame(rov_cam1,client_socket,'1')
		ReadSendFrame(rov_cam2,client_socket,'2')
		#	start_time = time.time()