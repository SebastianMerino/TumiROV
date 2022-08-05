import serial

class Propulsores():
    def __init__(self,port) -> None:
        #self.ser = serial.Serial(port = '/dev/ttyUSB0', baudrate=115200, timeout=5)
        self.rpm = 0
        self.MAX_RPM = 5000

    setCW = 0x0041000000
    setCCW = 0x0042000000
    def set_speed_prop(self,rpm,ID):
        """ Envía una velocidad de giro en RPM a un propulsor según su ID.
        RPM > 0: Counter Clock Wise, RPM < 0: Clock Wise """
        end = ID + 0x36
        maskCW = (ID << 32) | Propulsores.setCW | end
        maskCCW = (ID << 32) | Propulsores.setCCW | end
        if rpm == 0:
            #self.ser.write(maskCCW.to_bytes(5,'big'))
            #self.ser.write(maskCW.to_bytes(5,'big'))
            print(hex(maskCCW))
            print(hex(maskCW))
        else:
            if rpm > 0:
                packet = maskCCW | rpm<<8
            else:
                packet = maskCW | (-rpm)<<8
            #self.ser.write(packet.to_bytes(5,'big'))
            print(hex(packet))

    def set_speed_ROV(self,rpm):
        """ Manda la velocidad RPM en el sentido para que
        el ROV suba. Si la RPM es negativa, el ROV bajará """
        self.set_speed_prop(rpm,0x61)
        self.set_speed_prop(-rpm,0x62)
        self.rpm = rpm

    def set_vel_vertical(self,ax):
        """ Manda la velocidad normalizada, positiva hacia arriba """
        rpm = int(self.MAX_RPM * ax)
        self.set_speed_prop(rpm,0x61)
        self.set_speed_prop(-rpm,0x62)
        self.rpm = rpm