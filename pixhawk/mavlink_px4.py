from vehicle import Vehicle
from puertosUSB import buscar_puerto

puerto = buscar_puerto('MAVLink')
PX4 = Vehicle(puerto)

PX4.arm()
try:
    while True:
        canal = input('Canal: ')
        pwm = input('PWM en us: ')
        PX4.set_servo_pwm(int(canal),int(pwm))
        pass
finally:
    PX4.disarm()
    PX4.close_conn()

# PX4.start_data_rx()
# Aquí puedes recibir datos
# PX4.stop_data_rx()

