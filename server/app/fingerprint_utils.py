import time
import serial
import adafruit_fingerprint


# import board
# uart = busio.UART(board.TX, board.RX, baudrate=57600)

# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi and hardware UART:
# uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi 3 with pi3-disable-bt
# uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

##################################################


def capture_fingerprint_image():
    """Capture a fingerprint image and return it."""
    fingerprint_images = []

    for attempt in range(2):
        if attempt == 0:
            print("Place finger on sensor...", end="")
        else:
            print("Place same finger again...", end="")
        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return None
            else:
                print("Other error")
                return None

        # Capture the fingerprint image data
        fingerprint_image = finger.get_fpdata(sensorbuffer="image")
        fingerprint_images.append(fingerprint_image)

    # Check if both captured images are identical
    if fingerprint_images[0] == fingerprint_images[1]:
        return fingerprint_images[0]
    else:
        print("Fingerprint images do not match.")
        return None