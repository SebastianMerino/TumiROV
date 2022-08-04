import serial, threading

class Sonda:
	input_bytes = 'cmd>'.encode()
	keys = ['press','temp','cond','sal','O2sat','O2ppm','pH','time']

	def __init__(self,port):
		"""
		Inicializa el puerto serial y otras variables
		"""
		self.ser = serial.Serial(port=port, baudrate=38400)
		self.data_dict = None
		self.data_ready = False

	def config(self):
		""" Configura sonda para adquisicion en tiempo real """
		print('Iniciando sonda ...')
		self.ser.write('a'.encode()) # Cualquier tecla para empezar comunicacion
		self.ser.read_until(Sonda.input_bytes)
		self.ser.write('1'.encode()) # Data acquisition
		self.ser.read_until(Sonda.input_bytes)
		self.ser.write('1'.encode()) # Real-time data acquisition
		self.ser.read_until()
		self.ser.write('a'.encode()) # Cualquier tecla para empezar
		print('Sonda lista para enviar datos!')
	
	def start(self):
		""" Empieza el thread de adquisición """
		self.ser.timeout = 1
		self.running = True
		self.ser.write('a'.encode())	# Cualquier tecla para empezar comunicacion
		self.t = threading.Thread(target=self.update)
		self.t.start()
		# Espera a que esté listo el primer dato 
		while not self.data_ready:
			pass
	
	def update(self):
		""" Actualiza datos adquiridos """
		self.ser.reset_input_buffer()
		self.ser.read_until()
		while self.running:
			raw = self.ser.read_until() # Waits until new line
			data = raw.decode()

			# Descarta lineas inutiles
			if len(data)<3:
				continue	# linea con solo espacios
			if ord(data[-3]) > ord('9'):
				continue	# linea sin cifra al final
			data_arr = data.split()
			
			# Convierte a dict
			for j in range(7):
				data_arr[j] = float(data_arr[j])
			self.data_dict = dict(zip(Sonda.keys,data_arr))
			
			self.data_ready = True

	def stop(self):
		""" Detiene el thread de adquisición """
		self.running = False
		self.t.join()

	def shutdown(self):
		""" Apaga la sonda """
		print('Apagando sonda ...')
		self.ser.write(chr(27).encode())
		self.ser.read_until(Sonda.input_bytes)
		self.ser.write(chr(27).encode())
		self.ser.read_until(Sonda.input_bytes)
		self.ser.write(chr(27).encode())
		print('Sonda apagada!')
		self.ser.close()