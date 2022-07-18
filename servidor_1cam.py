import socket, cv2, pickle, struct

fuente1 = "rtsp://192.168.226.202:554"

host_ip = '192.168.226.100'
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(socket_address)	# Socket Bind
server_socket.listen(5) 			# Socket Listen
print("LISTENING AT:",socket_address)

client_socket,addr = server_socket.accept()
if client_socket:
	print('GOT CONNECTION FROM:',addr)
	rov_cam1 = cv2.VideoCapture(fuente1)
	
	while(rov_cam1.isOpened()):
		ret,frame = rov_cam1.read()
			
		if ret == True:
			# Pack size of frame + frame
			#frame = cv2.resize(frame,(176,144))	
			a = pickle.dumps(frame)
			message = struct.pack("Q",len(a))+a
			client_socket.sendall(message)
			