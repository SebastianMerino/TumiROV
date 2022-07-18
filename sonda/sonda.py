import serial, json, threading

class Sonda:
	input_bytes = 'cmd>'.encode()
	keys = ['press','temp','cond','sal','O2sat','O2ppm','pH','time']

	def __init__(self):
		# Configuring serial connections
		self.ser = serial.Serial(
			port='COM5',
			baudrate=38400,
			timeout=100,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)
		self.data_arr_str = None
		self.data_json = None
		self.data_ready = False

	# Configurar sonda para adquisicion en tiempo real
	def config(self):
		print('Iniciando sonda ...')
		self.ser.write('a'.encode()) # Cualquier tecla para empezar comunicacion
		self.ser.read_until(Sonda.input_bytes)
		self.ser.write('1'.encode()) # Data acquisition
		self.ser.read_until(Sonda.input_bytes)
		self.ser.write('1'.encode()) # Real-time data acquisition
		self.ser.read_until()
		self.ser.write('a'.encode()) # Cualquier tecla para empezar
		print('Sonda lista para enviar datos!')
	
	# Empieza el thread de adquisición
	def start(self):
		self.ser.timeout = 10
		self.running = True
		self.ser.write('a'.encode())	# Cualquier tecla para empezar comunicacion
		tSonda = threading.Thread(target=self.update)
		tSonda.daemon = True
		tSonda.start()
		# Espera a que esté listo el primer dato 
		while not self.data_ready:
			pass
	
	# Actualiza datos adquiridos
	def update(self):
		while self.running:
			self.ser.reset_input_buffer()
			self.ser.read_until()
			raw = self.ser.read_until() # Waits until new line
			data = raw.decode()

			# Descarta lineas inutiles
			if len(data)<3:
				continue
			if ord(data[-3]) > ord('9'):
				continue	# si no es una cifra
			self.data_arr_str = data.split()
			
			# Convierte a json
			data_arr = []
			for j in range(8):
				if j!= 7:
					data_arr.append(float(self.data_arr_str[j]))
				else:
					data_arr.append(self.data_arr_str[7])
			data_dict = dict(zip(Sonda.keys,data_arr))
			self.data_json = json.dumps(data_dict)
			
			self.data_ready = True

	# Para el thread de adquisición
	def stop(self):
		self.running = False

	# Apagar sonda
	def shutdown(self):
		print('Apagando sonda ...')
		self.ser.write(chr(27).encode())
		self.ser.read_until(Sonda.input_bytes)
		self.ser.write('0'.encode())
		self.ser.read_until(Sonda.input_bytes)
		self.ser.write('0'.encode())
		print('Sonda apagada!')
		self.ser.close()