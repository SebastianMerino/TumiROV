from sonda import Sonda
import time
import requests
import json

idronaut = Sonda()
#idronaut.config()

idronaut.start()

time_start = time.time()

while time.time() - time_start < 5:
    #(str_arr,data_json) = idronaut.read_data()
    print(idronaut.data_arr_str)
    time.sleep(1)

idronaut.stop()