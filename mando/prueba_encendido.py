from propulsores import Propulsores
import time

puerto = input('Ingrese puerto USB: ')
prop = Propulsores('/dev/ttyUSB'+puerto)

print('Intentando encender propulsores...')
prop.set_speed_prop(100,0x61)
prop.set_speed_prop(100,0x62)
time.sleep(10)