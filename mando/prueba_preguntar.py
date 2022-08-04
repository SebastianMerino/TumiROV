from propulsores import Propulsores
import time

puerto = input('Ingrese puerto USB: ')
prop = Propulsores('/dev/ttyUSB'+puerto)

print('Intentando pedir velocidad...')
ser = prop.ser
packet = 0x6150000097
ser.write(packet.to_bytes(5,'big'))
data = ser.recv()
print(data)