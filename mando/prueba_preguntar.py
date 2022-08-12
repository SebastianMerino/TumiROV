import serial

puerto = 'COM8'
ser = serial.Serial(port = puerto, baudrate=115200, timeout=3)

while True:
	packet = int(input('Hex input: '),16)
	ser.write(packet.to_bytes(5,'big'))
	data = ser.read(5)
	print(hex(int.from_bytes(data,'big')))

# data = ser.recv(5)
# num = int.from_bytes(data,"big")
# print(hex(num))