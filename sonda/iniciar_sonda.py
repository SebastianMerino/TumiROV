import serial

# Configuring serial connections
ser = serial.Serial(
    port = 'COM5',
    baudrate=38400,
    timeout=100,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

input_bytes = 'cmd>'.encode()

with ser: 
	print('Iniciando ...')
	ser.write('a'.encode()) # Cualquier tecla para empezar comunicacion

	ser.read_until(input_bytes)
	ser.write('1'.encode()) # Data acquisition

	ser.read_until(input_bytes)
	ser.write('1'.encode()) # Real-time data acquisition
	
	ser.write('a'.encode()) # Cualquier tecla para empezar

	print('Sonda lista para recibir datos!')