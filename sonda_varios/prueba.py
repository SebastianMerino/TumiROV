from sonda import Sonda
from puertosUSB import buscar_puerto
import time

hwid = '0403:6001'
idronaut = Sonda(buscar_puerto(hwid))
idronaut.config()
idronaut.start()

time_start = time.time()

while time.time() - time_start < 5:
    print(idronaut.data_dict)
    time.sleep(0.01)

idronaut.stop()
idronaut.shutdown()