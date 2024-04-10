###############################################################################
#
# File: rfid_reader.py
#
# Author: Isaac Ingram
#
# Purpose: Offer a way to interface with the RFID reader
#
###############################################################################
import platform

USE_RFID = False

# Check if the NFC reader can be used at all
if platform.system() == "Linux" and "rpi" in platform.uname().release:
    USE_RFID = True
    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522


def main():

    # Check if RFID can be used
    if USE_RFID:

        reader = SimpleMFRC522()
        try:
            while True:
                tag_uid, _ = reader.read()
        except KeyboardInterrupt:
            print("Control+C pressed, exiting program")
        finally:
            GPIO.cleanup()


if __name__ == '__main__':
    main()
