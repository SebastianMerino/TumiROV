from propulsores import *
from serial.tools.list_ports import grep
from jetson import JetsonPin
from vehicle import Vehicle

# ------------------------- SENSORES -------------------------------
# Puertos USB
def buscar_puerto(name):
    return next(grep(name)).device

# Propulsores
props = Propulsores(buscar_puerto("AR0K003I"))
Propulsor.MAX_RPM = 1000
props.start_tx()

# Pixhawk
PX4 = Vehicle(buscar_puerto('Pixhawk'))
PX4.MAX_PWM = 1300
PX4.arm()
PX4.start_rx()

# Luces
luces = JetsonPin(11)

# -----------------------------------------------------------------

# --------------------------------- MAIN -------------------------------------
if __name__ == '__main__':
	try:
		while True:
			boton = input()
			if boton == 'w':
				PX4.avanzar(1)
			elif boton == 's':
				PX4.avanzar(-1)
			
			if boton == 'd':
				PX4.lateral(1)
			elif boton == 'a':
				PX4.lateral(-1)
			
			if boton == 'l':
				PX4.girar(1)
			elif boton == 'j':
				PX4.girar(-1)
			
			if boton == 'i':
				props.subir(1)
			elif boton == 'k':
				props.subir(-1)
			
			if boton == ' ':
				props.subir(0)
				PX4.girar(0)
				PX4.avanzar(0)
				PX4.lateral(0)

			#Luces
			if boton == 'z':
				luces.switch()
	finally:
		props.stop_tx()
		props.close()
		luces.close()
		PX4.stop_rx()
		PX4.disarm()
		PX4.close_conn()