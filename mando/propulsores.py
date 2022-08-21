import serial, threading
#import time

class Propulsores():
    def __init__(self,port):
        """ Inicializa propulsores y puerto serial por el que se comunican """
        self.propIzq = Propulsor(0x61)
        self.propDer = Propulsor(0x62)
        self.ser = serial.Serial(port = port, baudrate=115200, timeout=5)
        self.Tx = False
        print('Propulsores verticales listos!')

    def start_tx(self):
        """ Inicia el thread de Tx de paquetes """
        self.thrTx = threading.Thread(target=self.update, daemon=True)
        self.Tx = True
        self.thrTx.start()
    
    def update(self):
        """ Actualiza los datos enviados a los motores """
        while self.Tx:
            self.ser.write(self.propDer.packet)
            self.ser.write(self.propIzq.packet)
            #print(hex(self.propDer.packet))
            #print(hex(self.propIzq.packet),'\n')
            #time.sleep(1)

    def stop_tx(self):
        """ Finaliza el thread de Tx """
        self.Tx = False
        self.thrTx.join()

    def subir(self,vel):
        """ Manda la velocidad normalizada, positiva hacia arriba """
        self.propIzq.set_speed_norm(vel)
        self.propDer.set_speed_norm(-vel)
    
    def close(self):
        """ Apaga motores y cierra el puerto serial """
        self.ser.write(self.propDer.brakeCommand)
        self.ser.write(self.propIzq.brakeCommand)
        self.ser.close()
        print('Propulsores verticales apagados!')

class Propulsor():
    MAX_RPM = 3000      # Puede ser 5k o 7k
    def __init__(self, ID):
        """ Modifica las mascaras segun el ID e inicializa el RPM """
        self.setCWmask = (ID << 32) | 0x0041000000 | (ID + 0x36)
        self.setCCWmask = (ID << 32) | 0x0042000000 | (ID + 0x36)
        self.brakeCommand = (ID << 32) | 0x0043000000 | (ID + 0x36)
        self.vel = 0
        self.packet = self.brakeCommand
    
    def set_speed_norm(self,vel):
        """
        Modifica la velocidad del motor en el mensaje a enviar 
        vel: velocidad normalizada de -1 a 1 (negativo CW, positivo CCW)
        NOTA: el minimo RPM para que se mueva es alrededor de 390
        """
        rpm = int(vel*Propulsor.MAX_RPM)
        if rpm == 0:
            packet = self.brakeCommand
        else:
            if rpm > 0:
                packet = self.setCCWmask | rpm<<8
            else:
                packet = self.setCWmask | (-rpm)<<8
        self.packet = packet
        self.vel = vel
