import dronekit
from numpy import pi
import time
from pymavlink import mavutil
import math
vehicle = dronekit.connect('COM4', wait_ready=True)

def vel_callback(self,attr_name,value):
    print("Velocidad: ", value )

def orient_callback(self,attr_name,att):
    print("Orientación: ", [att.pitch*180/pi, att.yaw*180/pi, att.roll*180/pi])

#Add observers
#vehicle.add_attribute_listener('velocity', vel_callback)
#vehicle.add_attribute_listener('attitude', orient_callback)
#time.sleep(30)

vehicle.close()
#--------------     TO DO   ------------
#   - Chequear si la velocidad es absoluta (segun brujula) o relativa
#   - Si es relativa corregir con el yaw
#   