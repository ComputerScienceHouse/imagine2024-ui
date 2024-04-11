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
import paho.mqtt.client as mqtt
import database

USE_RFID = False
MQTT_BROKER_ADDRESS = "localhost"
MQTT_BROKER_PORT = 1883


# Check if the NFC reader can be used at all
if platform.system() == "Linux" and "rpi" in platform.uname().release:
    USE_RFID = True
    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522


def main():

    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.connect(MQTT_BROKER_ADDRESS, port=MQTT_BROKER_PORT)

    # Check if RFID can be used
    if USE_RFID:

        reader = SimpleMFRC522()
        try:
            while True:
                tag_uid, _ = reader.read()
                user = database.get_user(user_token=tag_uid)
                mqtt_client.publish("rfid/user", str(user))

        except KeyboardInterrupt:
            print("Control+C pressed, exiting program")
        finally:
            GPIO.cleanup()


if __name__ == '__main__':
    main()
