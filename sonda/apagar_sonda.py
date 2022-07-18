import serial

# Configuring serial connections
ser = serial.Serial(
	port = 'COM5',
	baudrate=38400,
	timeout=1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)
input_bytes = 'cmd>'.encode()

with ser:
	print('Apagando sonda ...')
	ser.write(chr(27).encode())
	
	ser.read_until(input_bytes)
	ser.write('0'.encode())

	ser.read_until(input_bytes)
	ser.write('0'.encode())
	
	ser.read_until('Completed'.encode())
	print('Sonda apagada!')
