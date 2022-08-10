import serial

class Propulsores():
    def __init__(self,port):
        """ Inicializa propulsores y puerto serial por el que se comunican """
        self.MAX_RPM = 5000
        self.prop61 = Propulsor(0x61)
        self.prop62 = Propulsor(0x62)
        #Propulsor.ser = serial.Serial(port = port, baudrate=115200, timeout=5)

    def set_vel_vertical(self,ax):
        """ Manda la velocidad normalizada, positiva hacia arriba """
        rpm = int(self.MAX_RPM * ax)
        self.prop61.set_speed(rpm)
        self.prop62.set_speed(-rpm)
    
    def close(self):
        """ Apaga motores y cierra el puerto serial """
        self.prop61.set_speed(0)
        self.prop62.set_speed(0)
        Propulsor.ser.close()
        print('Propulsores verticales apagados!')

class Propulsor():
    ser = None
    setCWmask = 0x0041000000
    setCCWmask = 0x0042000000
    def __init__(self, ID):
        """ Modifica las máscaras según el ID e inicializa el RPM """
        self.setCWmask = (ID << 32) | Propulsor.setCWmask | (ID + 0x36)
        self.setCCWmask = (ID << 32) | Propulsor.setCCWmask | (ID + 0x36)
        self.rpm = 0
    
    def set_speed(self,rpm: int):
        """ Modifica la velocidad del motor """
        if rpm == 0:
            #Propulsor.ser.write(self.setCWmask.to_bytes(5,'big'))
            #Propulsor.ser.write(self.setCCWmask.to_bytes(5,'big'))
            print(hex(self.setCWmask))
            print(hex(self.setCCWmask))
        else:
            if rpm > 0:
                packet = self.setCCWmask | rpm<<8
            else:
                packet = self.setCWmask | (-rpm)<<8
            #Propulsor.ser.write(packet.to_bytes(5,'big'))
            print(hex(packet))
        self.rpm = rpm
