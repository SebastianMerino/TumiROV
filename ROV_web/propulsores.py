import serial

class Propulsores():
    def __init__(self,port):
        """ Inicializa propulsores y puerto serial por el que se comunican """
        self.propIzq = Propulsor(0x61)
        self.propDer = Propulsor(0x62)
        Propulsor.ser = serial.Serial(port = port, baudrate=115200, timeout=5)

    def set_vel_vertical(self,vel):
        """ Manda la velocidad normalizada, positiva hacia arriba """
        self.propIzq.set_speed_norm(vel)
        self.propDer.set_speed_norm(-vel)
    
    def close(self):
        """ Apaga motores y cierra el puerto serial """
        self.propIzq.set_speed_norm(0)
        self.propDer.set_speed_norm(0)
        Propulsor.ser.close()
        print('Propulsores verticales apagados!')

class Propulsor():
    ser = None          # Puerto serial
    setCWmask = 0x0041000000
    setCCWmask = 0x0042000000
    brakeCommand = 0x0043000000
    MAX_RPM = 3000      # Puede ser 5k o 7k
    def __init__(self, ID):
        """ Modifica las máscaras según el ID e inicializa el RPM """
        self.setCWmask = (ID << 32) | Propulsor.setCWmask | (ID + 0x36)
        self.setCCWmask = (ID << 32) | Propulsor.setCCWmask | (ID + 0x36)
        self.brakeCommand = (ID << 32) | Propulsor.brakeCommand | (ID + 0x36)
        self.vel = 0
    
    def set_speed_norm(self,vel):
        """
        Modifica la velocidad del motor 
        vel: velocidad normalizada de -1 a 1 (negativo CW, positivo CCW)
        NOTA: el mínimo RPM para que se mueva es alrededor de 390
        """
        rpm = int(vel*Propulsor.MAX_RPM)
        if rpm == 0:
            packet = self.brakeCommand
        else:
            if rpm > 0:
                packet = self.setCCWmask | rpm<<8
            else:
                packet = self.setCWmask | (-rpm)<<8
        Propulsor.ser.write(packet.to_bytes(5,'big'))
        #print(hex(packet))
        self.vel = vel
