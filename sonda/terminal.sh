#!/bin/bash
echo "Puertos disponibles: "
python -m serial.tools.list_ports
read -p "Ingresa el port path: " port
python -m serial.tools.miniterm $port 38400 --exit-char 101