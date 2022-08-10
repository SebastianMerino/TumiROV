import serial

puerto = input('Puerto o path USB?: ')
ser = serial.Serial(port = puerto, baudrate=115200, timeout=5)

print('Intentando pedir velocidad...')
packet = 0x6150000097
ser.write(packet.to_bytes(5,'big'))
while True:
	data = ser.recv(1)
	print(data)

# data = ser.recv(5)
# num = int.from_bytes(data,"big")
# print(hex(num))