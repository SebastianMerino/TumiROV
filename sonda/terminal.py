import threading
import serial, json, keyboard
from flask import Flask, render_template
import time

data_arr_str = []

# Configuring serial connections
ser = serial.Serial(
	port = '/dev/ttyUSB0',
	baudrate=38400,
	timeout=3,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

def leer():
	while True:
		raw = ser.read_until()
		data = raw.decode()
		print(data, end='')


with ser:
	# Cualquier tecla para empezar comunicacion 
	ser.write('a'.encode())	
	t = threading.Thread(target=leer)
	t.start()
	while True:
		cmd = input()
		ser.write(cmd.encode())


