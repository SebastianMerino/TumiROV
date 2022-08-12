import serial, time

port = input('Ingrese el puerto USB: ')
ser = serial.Serial(port = port, baudrate=38400, timeout=1)
input_bytes = 'cmd>'.encode()

with ser: 
	print('Iniciando ...')
	ser.write('a'.encode()) # Cualquier tecla para empezar comunicacion

	raw = ser.read_until(input_bytes)
	print(raw.decode(),end='')
	time.sleep(1)
	ser.write('1'.encode()) # Data acquisition

	raw = ser.read_until(input_bytes)
	print(raw.decode(),end='')
	time.sleep(1)
	ser.write('1'.encode()) # Real-time data acquisition
	
	time.sleep(1)
	raw = ser.read_until('leave'.encode())
	print(raw.decode(),end='')
	ser.write('a'.encode()) # Cualquier tecla para empezar
	print('\n\nSonda lista para recibir datos!')