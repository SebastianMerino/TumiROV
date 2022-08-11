import RPi.GPIO as GPIO

class JetsonPin:
    """
    Clase utilizada para el uso de los pines GPIO de la Jetson.
    Actualmente en el ROV las luces están en el pin 11.
    """
    def __init__(self, pin: int) -> None:
        self.output_pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.output_pin, GPIO.OUT, initial=GPIO.LOW)
        self.encendido = False
    def encender(self):
        GPIO.output(self.output_pin, GPIO.HIGH)
        self.encendido = True
    def apagar(self):
        GPIO.output(self.output_pin, GPIO.HIGH)
        self.encendido = False
    def switch(self):
        if self.encendido:
            self.apagar()
        else:
            self.encender()
    def close(self):
        GPIO.cleanup()