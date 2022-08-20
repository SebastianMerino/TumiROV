#!/bin/bash
# Permite abrir el terminal de la sonda en cualquier computadora con Linux
echo "Puertos disponibles: "
python -m serial.tools.list_ports -v
read -p "Ingresa el port: " port
path="/dev/ttyUSB"
python -m serial.tools.miniterm "$path$port" 38400 --exit-char 101