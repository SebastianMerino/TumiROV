import serial

puerto = input('Puerto o path USB?: ')
ser = serial.Serial(port = puerto, baudrate=115200, timeout=5)

id = int(input('ID en hex?: '),16)
setCWmask = (id << 32) | 0x0041000000 | (id + 0x36)
setCCWmask = (id << 32) | 0x0042000000 | (id + 0x36)

while True:
	rpm = int(input('RPM? '))
	sentido = input('CCW? (y/n): ')
	if sentido == 'y':
		packet = setCCWmask | rpm<<8
	elif sentido == 'n':
		packet = setCWmask | rpm<<8
	ser.write(packet.to_bytes(5,'big'))