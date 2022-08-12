import serial, time

port = input('Ingrese el puerto USB: ')
ser = serial.Serial(port = port, baudrate=38400, timeout=1)
input_bytes = 'cmd>'.encode()

with ser:
	print('Apagando sonda ...')
	ser.write(chr(27).encode())
	
	raw = ser.read_until(input_bytes)
	print(raw.decode(),end='')
	time.sleep(1)
	ser.write(chr(27).encode())

	raw = ser.read_until(input_bytes)
	print(raw.decode(),end='')
	time.sleep(1)
	ser.write(chr(27).encode())
		
	raw = ser.read_until('Completed'.encode())
	print(raw.decode(),end='')
	print('Sonda apagada!')