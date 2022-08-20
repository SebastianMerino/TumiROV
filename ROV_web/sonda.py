"""
Módulo para manejar la recepción de datos de la sonda
Ocean Seven 310 de Idronaut.
"""
import serial, threading
from math import pi, sin

class Sonda:
	"""" Clase utilizada para gestionar la recepción de datos de la sonda """
	input_bytes = 'cmd>'.encode()
	keys = ['press','temp','cond','sal','O2sat','O2ppm','pH','time']

	def __init__(self,port):
		"""	Inicializa el puerto serial y otras variables """
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
		self.t = threading.Thread(target=self.update, daemon=True)
		self.t.start()
		# Espera a que esté listo el primer dato 
		while not self.data_ready:
			pass
	
	def update(self):
		""" Actualiza datos adquiridos """
		# Anteriormente hubo errores de modo que cada vez que se vuelve
		# al thread la línea está a la mitad. Se soluciona al resetear 
		# el buffer y leer hasta el cambio de línea dentro del loop.
		while self.running:
			self.ser.reset_input_buffer()
			self.ser.read_until()
			raw = self.ser.read_until() # Lee línea
			data = raw.decode()

			# Descarta lineas inutiles
			if len(data)<10:
				continue	# linea con solo espacios
			if ord(data[-3]) > ord('9'):
				continue	# linea sin cifra al final
			data_arr = data.split()
			
			# Convierte a diccionario
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

def calc_profundidad(p,lat):
	"""
	Calcula la profundidad a la que está sumergido el ROV en función
	de la presión en dbar y la latitud (positiva). Con la fórmula de
	"Depth-pressure relationships in the oceans and seas" por
	Claude C. Leroy y Francois Parthiot
	"""
	c1,c2,c3,c4 = 9.7266, -2.2512E-5, 2.28E-10, -1.8E-15
	lat = 12.5
	g = 9.7803 * (1+ 5.3E-3*sin(lat*pi/180))
	z = (c1*p + c2*p**2 + c3*p**3 + c4*p**4)/(g + 1.1E-6*p)
	corr = p/(p+100) + 5.7E-4*p
	return z+corr