@echo off
ECHO Puertos disponibles:
py -m serial.tools.list_ports
set /p "port=Enter port: "
py -m serial.tools.miniterm %port% 38400 --exit-char 101