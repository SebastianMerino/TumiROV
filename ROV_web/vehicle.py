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
		# Atributos de la IMU
		self.attitude = []
		self.velocity = []
		self.vel_mod = 0
		self.time_boot = 0
		# Datos de los motores
		self.pwm = [1100,1100,1100,1100,1100,1100,1100,1100]
		self.motors = [0,0,0,0]
		self.MAX_PWM = 1700
		# Threads de transmision y recepcion
		self.Rx = False
		self.Tx = False
		# Espera a la conexion
		self.master.wait_heartbeat()

	# ------------------------------ MOTORES ------------------------------
	def arm(self,timeout=5):
		"""
		Envía el comando para habilitar los motores
		Espera a que estén habilitados según timeout
		Empieza thread de transmisión de datos a los motores
			timeout: Tiempo máximo de espera.
		"""
		self.master.mav.command_long_send(
		self.master.target_system, self.master.target_component,
		mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0,
		1, 0, 0, 0, 0, 0, 0)

		# Espera a que los motores esten habilitados
		print("Armando motores horizontales...")
		start_time = time.time()
		while time.time()-start_time < timeout or not self.master.motors_armed():
			self.master.wait_heartbeat()
		
		if self.master.motors_armed():
			# Empieza los threads de transmisión para actualizar las pwm			
			self.Tx = True
			self.thrTx  = threading.Thread(target=self.update_pwm, daemon=True)
			self.thrTx .start()
			# Esperamos a que se envíen las pwm de 1100
			self.master.wait_heartbeat()
			print('Motores horizontales listos!')
		else:
			print("No se pudo armar los motores, intentando nuevamente...")
			self.arm()
			# raise Exception("No se pudo iniciar el motor")
			# NOTA: A veces los motores no se pueden iniciar por alguna razon
			#       que desconozco. Sin embargo, al segundo intento, funciona.

	def update_pwm(self):
		""" Actualiza la PWM de un canal FMU """
		while self.Tx:
			for i in reversed(range(8)):
				# Los canales FMU son del 9-16, las pwm estan en pwm[i]
				self.master.set_servo(i+9,self.pwm[i])

	def set_vel_motor(self,motor_n,vel):
		"""
		Coloca uno de los 4 motores a una velocidad (normalizada de -1 a 1)
		"""
		rango = self.MAX_PWM - 1100
		if vel>=0:
			pwm = int(vel*rango) + 1100
			self.pwm[motor_n+3] = 1100
		else:
			pwm = int(-vel*rango) + 1100
			self.pwm[motor_n+3] = 1900
		self.pwm[motor_n-1] = pwm
		self.motors[motor_n-1] = vel

	def disarm(self):
		""" Termina el thread de transmision y 
		apaga todos los motores (PWM 0) """
		for i in range(1,5):
			self.set_vel_motor(i,0)
		# Espera
		self.master.wait_heartbeat()
		self.master.wait_heartbeat()
		
		self.Tx = False
		self.thrTx.join()
		print("Propulsores horizontales apagados")

	def avanzar(self,vel):
		self.set_vel_motor(1,-vel)
		self.set_vel_motor(2,-vel)
		self.set_vel_motor(3,-vel)
		self.set_vel_motor(4,-vel)

	def lateral(self,vel):
		self.set_vel_motor(1,vel)
		self.set_vel_motor(2,-vel)
		self.set_vel_motor(3,-vel)
		self.set_vel_motor(4,vel)

	def girar(self,vel):
		self.set_vel_motor(1,vel)
		self.set_vel_motor(2,-vel)
		self.set_vel_motor(3,vel)
		self.set_vel_motor(4,-vel)

	def request_message_interval(self, message_id: int, frequency_hz: float):
		"""
		Solicita el envío periódico de un tipo de mensaje.
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
		while self.Rx:
			msg_att = self.master.recv_match(type='ATTITUDE')
			msg_gp = self.master.recv_match(type='GLOBAL_POSITION_INT')
			if msg_att is not None:
				att_dict = msg_att.to_dict()
				#print(att_dict)
				self.attitude = [att_dict['roll'], att_dict['pitch'], att_dict['yaw']]
				self.time_boot = att_dict['time_boot_ms']/1000
			if msg_gp is not None:
				global_pos = msg_gp.to_dict()
				vN = global_pos['vx']/100
				vE = global_pos['vy']/100
				vD = global_pos['vz']/100
				self.velocity = [vN,vE,vD]
				self.vel_mod = (vN**2+vE**2+vD**2)**.5

	def start_rx(self):
		""" Inicia el thread de adquisición de datos. """
		master = self.master
		# Configurar mensajes a frecuencia de 30 Hz
		self.request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT, 30)
		self.request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE, 30)

		att_dict = master.recv_match(type='ATTITUDE',blocking=True).to_dict()
		self.attitude = [att_dict['roll'], att_dict['pitch'], att_dict['yaw']]
		global_pos = master.recv_match(type='GLOBAL_POSITION_INT',blocking=True).to_dict()
		self.velocity = [global_pos['vx']/100, global_pos['vy']/100, global_pos['vz']/100]

		self.Rx = True
		self.thrRx = threading.Thread(target=self.receive_data, daemon=True)
		self.thrRx.start()
		print("Comenzado el thread de adquisición de la Pixhawk")

	def stop_rx(self):
		""" Termina el thread de adquisición y espera a que este acabe. """
		self.Rx = False
		self.thrRx.join()
		print("Terminado el thread de adquisición de la Pixhawk")

	def reboot(self):
		""" Reinicia la Pixhawk. """
		self.master.reboot_autopilot()

	def close_conn(self):
		""" Cierra la conexión. """
		self.master.close()
		print("Conexion con la Pixhawk terminada")
