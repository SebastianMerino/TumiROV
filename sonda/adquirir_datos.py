import serial, json, keyboard
from flask import Flask, render_template
import time

data_arr_str = []

# Configuring serial connections
ser = serial.Serial(
	port = 'COM5',
	baudrate=38400,
	timeout=10,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

with ser:
	# Cualquier tecla para empezar comunicacion 
	ser.write('a'.encode())	
	ser.read_until()
	while True:
		raw = ser.read_until()
		data = raw.decode()
		print(data)
		if len(data)<3:
			continue
		if ord(data[-3]) < ord('0') or ord(data[-3]) > ord('9'):
			continue
		if keyboard.is_pressed(chr(27)):
			break

		data_str_arr = data.split()
		#print(data_str_arr)
		data_arr = []
		for j in range(8):
			if j!= 7:
				data_arr.append(float(data_str_arr[j]))
		keys = ['pressure','temperature','conductivity','salinity','O2%Sat','O2ppm','pH','time']
		python_dic = dict(zip(keys,data_arr))
		data_json = json.dumps(python_dic, indent=4)


