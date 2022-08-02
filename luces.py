import RPi.GPIO as GPIO
import time

# Pin Definitions
output_pin = 22
def main():
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)

    print("Starting demo now! Press CTRL+C to exit")
    curr_value = GPIO.HIGH
    try:
        print("Outputting {} to pin {}".format(curr_value, output_pin))
        while True:
            time.sleep(3)
            # Toggle the output every second
            GPIO.output(output_pin, curr_value)
            curr_value = GPIO.HIGH
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()