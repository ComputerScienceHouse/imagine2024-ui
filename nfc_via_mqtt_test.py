###############################################################################
#
# File: nfc_via_mqtt_test.py
#
# Author: Isaac Ingram
#
# Purpose: Print RFID related data coming from the MQTT broker
#
###############################################################################

from utils.mqtt import MQTT as mqtt


def callback_func(user_data: str):
    print(user_data)


def main():
    client = mqtt()
    client.set_rfid_user_callback(callback_func)
    client.loop_forever()


if __name__ == '__main__':
    main()
