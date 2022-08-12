#!/bin/bash
# Permite abrir el terminal de la sonda en cualquier computadora con Linux
echo "Puertos disponibles: "
python -m serial.tools.list_ports -v
read -p "Ingresa el port path: " port
python -m serial.tools.miniterm $port 38400 --exit-char 101