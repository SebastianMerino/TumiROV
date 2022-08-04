@echo off
ECHO Puertos disponibles:
py -m serial.tools.list_ports
set /p "port=Ingresa el puerto: "
py -m serial.tools.miniterm %port% 38400 --exit-char 101