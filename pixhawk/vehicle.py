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
        self.time_boot = 0
        self.receiving = True

    def arm(self,timeout=5):
        """
        Envía el comando para habilitar los motores y espera a que estén habilitados
        args:
            timeout: Tiempo máximo de espera.
        """
        self.master.wait_heartbeat()
        self.master.mav.command_long_send(
        self.master.target_system, self.master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0,
        1, 0, 0, 0, 0, 0, 0)

        # wait until arming confirmed
        print("Armando motores...")
        start_time = time.time()
        while time.time()-start_time < timeout:
            self.master.wait_heartbeat()
            if self.master.motors_armed():
                print('Motores listos!')
                return
        
        # NOTA: A veces los motores no se pueden iniciar por alguna razon
        #       que desconozco. Sin embargo, al segundo intento, funciona.
        #       Por ello, en vez de enviar error, vuelvo a llamar a la
        #       función.
        # raise Exception("No se pudo iniciar el motor")
        print("No se pudo armar los motores, intentando nuevamente...")
        self.arm()

    def set_rc_channel_pwm(self,channel_id, pwm=1500):
        """ 
        Escribe comandos en los canales RC para manejar los motores.
        Yaw: 4, Forward: 5, Lateral: 6
        http://www.ardusub.com/developers/rc-input-and-output.html
        args:
            channel_id (TYPE): Channel ID.
            pwm (int): Channel pwm value 1100-1900
        """
        if channel_id < 1 or channel_id > 18:
            print("Channel does not exist.")
            return

        rc_channel_values = [65535 for _ in range(18)]
        rc_channel_values[channel_id - 1] = pwm
        self.master.mav.rc_channels_override_send(
            self.master.target_system,                # target_system
            self.master.target_component,             # target_component
            *rc_channel_values)                  # RC channel list, in microseconds.
    
    def disarm(self):
        """
        Envía el comando para deshabilitar los motores y espera
        a que estén deshabilitados.
        args:
            timeout: Tiempo máximo de espera.
        """
        self.master.wait_heartbeat()
        self.master.mav.command_long_send(
            self.master.target_system, self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0,
            0, 0, 0, 0, 0, 0, 0)

        # wait until disarming confirmed
        print("Desarmando motores")
        self.master.motors_disarmed_wait()
        print("Desarmados!")

    def avanzar(self,vel=0,duration=0.1):
        print("Avanzando...")
        pwm = int(vel*400 + 1500)
        start_time = time.time()
        while time.time()- start_time < duration:
            self.master.wait_heartbeat()
            self.set_rc_channel_pwm(5, pwm)
        #self.set_rc_channel_pwm(5, 1500)

    def girar(self,vel=0,duration=0.1):
        print("Girando...")
        pwm = int(vel*400 + 1500)
        start_time = time.time()
        while time.time() - start_time < duration:
            self.master.wait_heartbeat()
            self.set_rc_channel_pwm(4, pwm)

    def avanzar_lateral(self,vel=0,duration=0.1):
        print("De lado...")
        pwm = int(vel*400 + 1500)
        start_time = time.time()
        while time.time()- start_time < duration:
            self.master.wait_heartbeat()
            self.set_rc_channel_pwm(6, pwm)

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
                self.velocity = [global_pos['vx']/100, global_pos['vy']/100, global_pos['vz']/100]

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
