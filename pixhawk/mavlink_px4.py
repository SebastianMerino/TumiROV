from vehicle import Vehicle
from puertosUSB import buscar_puerto
import time

puerto = buscar_puerto('MAVLink')
PX4 = Vehicle(puerto)

# PX4.arm()
# try:
#     while True:
#         canal = input('Canal: ')
#         pwm = input('PWM en us: ')
#         PX4.set_servo_pwm(int(canal),int(pwm))
#         pass
# finally:
#     PX4.disarm()
#     PX4.close_conn()

PX4.start_rx()
try:
    while True:
        time.sleep(0.5)
        print('Velocity: ',PX4.velocity)
        print('Attitude: ', PX4.attitude)

finally:
    PX4.stop_rx()
    PX4.close_conn()

