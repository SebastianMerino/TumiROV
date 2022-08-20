from pymavlink import mavutil
import time
import threading

class Vehicle:
	"""
	Clase para manejar la comunicación entre la Pixhawk 4 y una computadora.
	Es necesario ingresar el puerto por el que está conectada.
	Incluye código adaptado de: http://www.ardusub.com/developers/pymavlink.html
	"""
	def __init__(self,port):
		"""
		Establece la conexión MAVlink e inicializa variables.
		"""
		self.master = mavutil.mavlink_connection(port, baud=115200)
		self.attitude = []
		self.velocity = []
		self.vel_mod = 0
		self.motors_vel = [0,0,0,0]
		self.time_boot = 0
		self.receiving = True
		self.MAX_PWM = 1700
		self.master.wait_heartbeat()

	def arm(self,timeout=5):
		"""
		Envía el comando para habilitar los motores y espera a que estén habilitados
		args:
			timeout: Tiempo máximo de espera.
		"""
		self.master.mav.command_long_send(
		self.master.target_system, self.master.target_component,
		mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0,
		1, 0, 0, 0, 0, 0, 0)

		# wait until arming confirmed
		print("Armando motores horizontales...")
		start_time = time.time()
		while time.time()-start_time < timeout or not self.master.motors_armed():
			self.master.wait_heartbeat()
		if self.master.motors_armed():
			print('Motores horizontales listos!')
		else:
			print("No se pudo armar los motores horizontales, intentando nuevamente...")
			self.arm()
			# raise Exception("No se pudo iniciar el motor")
			# NOTA: A veces los motores no se pueden iniciar por alguna razon
			#       que desconozco. Sin embargo, al segundo intento, funciona.
		
		for i in range(8):
			self.set_servo_pwm(i+1,0)
	
	def disarm(self):
		"""
		Envía el comando para deshabilitar los motores y espera
		a que estén deshabilitados.
		"""
		# Apaga todos los motores (PWM 0)
		for i in range(8):
			self.set_servo_pwm(i+1,0)
		print('Motores horizontales apagados!')

	def set_servo_pwm(self, servo_n, us):
		"""
		Sets 'servo_n' output PWM pulse-width.
			servo_n: PWM port to set from FMU PWM (1-8)
			us: PWM pulse-width in microseconds. Between 1100 and 1900
		"""
		self.master.set_servo(servo_n+8, us)

	def set_motor(self,n,vel):
		"""
		Coloca uno de los 4 motores a una velocidad (normalizada de -1 a 1)
		"""
		rango = self.MAX_PWM - 1100
		if vel>=0:
			pwm = vel*rango + 1100
			self.set_servo_pwm(n+4,1100)
			self.set_servo_pwm(n,pwm)
		else:
			pwm = (-vel)*rango + 1100
			self.set_servo_pwm(n+4,1900)
			self.set_servo_pwm(n,pwm)
		self.motors_vel[n-1] = vel

	def avanzar(self,vel):
		self.set_motor(1,vel)
		self.set_motor(2,vel)
		self.set_motor(3,vel)
		self.set_motor(4,vel)

	def lateral(self,vel):
		self.set_motor(1,vel)
		self.set_motor(2,vel)
		self.set_motor(3,vel)
		self.set_motor(4,vel)

	def girar(self,vel):
		self.set_motor(1,vel)
		self.set_motor(2,vel)
		self.set_motor(3,vel)
		self.set_motor(4,vel)
	
	def request_message(self, message_id: int):
		"""
		Solicita el envío de un solo mensaje.
		args:
			message_id: ID del mensaje, mavutil.mavlink.MAVLINK_MSG_ID_nombre
						https://mavlink.io/en/messages/common.html
		"""
		master = self.master
		master.mav.command_long_send(
			master.target_system, master.target_component,
			mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE, 0,
			message_id, # The MAVLink message ID
			0, 0, 0, 0, 0,# Unused parameters
			0, # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
		)

	def request_message_interval(self, message_id: int, frequency_hz: float):
		"""
		Solicita el envío periódico de un tipo de mensaje.
		args:
			message_id: ID del mensaje, mavutil.mavlink.MAVLINK_MSG_ID_nombre
						https://mavlink.io/en/messages/common.html
			frequency_hz: Frecuencia de envío
		"""
		master = self.master
		master.mav.command_long_send(
			master.target_system, master.target_component,
			mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
			message_id, # The MAVLink message ID
			1e6 / frequency_hz, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
			0, 0, 0, 0, # Unused parameters
			0, # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
		)

	def receive_data(self):
		""" Recibe datos de la Pixhawk constantemente. """
		while self.receiving:
			msg_att = self.master.recv_match(type='ATTITUDE')
			msg_gp = self.master.recv_match(type='GLOBAL_POSITION_INT')
			if msg_att is not None:
				att_dict = msg_att.to_dict()
				self.attitude = [att_dict['roll'], att_dict['pitch'], att_dict['yaw']]
				self.time_boot = att_dict['time_boot_ms']/1000
			if msg_gp is not None:
				global_pos = msg_gp.to_dict()
				vN = global_pos['vx']/100
				vE = global_pos['vy']/100
				vD = global_pos['vz']/100
				self.velocity = [vN,vE,vD]
				self.vel_mod = (vN**2+vE**2+vD**2)**.5

	def start_data_rx(self):
		""" Inicia el thread de adquisición de datos. """
		master = self.master
		# Configurar mensajes a frecuencia de 30 Hz
		self.request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT, 30)
		self.request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE, 30)


		att_dict = master.recv_match(type='ATTITUDE',blocking=True).to_dict()
		self.attitude = [att_dict['roll'], att_dict['pitch'], att_dict['yaw']]
		global_pos = master.recv_match(type='GLOBAL_POSITION_INT',blocking=True).to_dict()
		self.velocity = [global_pos['vx']/100, global_pos['vy']/100, global_pos['vz']/100]

		self.t = threading.Thread(target=self.receive_data, daemon=True)
		self.t.start()
		print("Transmitiendo datos de la Pixhawk!")

	def stop_data_rx(self):
		""" Termina el thread de adquisición y espera a que este acabe. """
		self.receiving = False
		self.t.join()

	def reboot(self):
		""" Reinicia la Pixhawk. """
		self.master.reboot_autopilot()

	def close_conn(self):
		""" Cierra la conexión. """
		self.master.close()
		print('Pixhawk desconectada!')

