import socket,cv2, pickle,struct

host_ip = '192.168.226.100'
port = 9999

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((host_ip,port)) # a tuple

data = b""
payload_size = struct.calcsize("Q")

while True:
	# Get message size
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024) # 4K
		if not packet:
			break
		data += packet
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack("Q",packed_msg_size)[0]
	
	# Receive and unpack frame
	while len(data) < msg_size+1:
		data += client_socket.recv(4*1024)
	cam_num = data[0]
	frame_data = data[1:msg_size+1]
	data  = data[msg_size+1:]
	frame = pickle.loads(frame_data, encoding='latin1')
	frame = cv2.resize(frame,(704,576))
	cv2.imshow("RECEIVING VIDEO FROM CAM"+chr(cam_num),frame)

	key = cv2.waitKey(1) & 0xFF
	if key == 27:
		break

client_socket.close()
cv2.destroyAllWindows()