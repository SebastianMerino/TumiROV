from sonda import Sonda
import time

idronaut = Sonda('COM5')
idronaut.config()
idronaut.start()

time_start = time.time()

while time.time() - time_start < 5:
    print(idronaut.data_dict)
    time.sleep(0.01)

idronaut.stop()
idronaut.shutdown()