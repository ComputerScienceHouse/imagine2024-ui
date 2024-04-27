###############################################################################
#
# File: mqtt.py
#
# Author: Isaac Ingram
#
# Purpose: Provide interface with MQTT broker
#
###############################################################################
import paho.mqtt.client as mqtt
from typing import Callable
from typing import Any
import database

MQTT_BROKER_ADDRESS = "localhost"
MQTT_BROKER_PORT = 1883


RFID_USER_TOPIC = "rfid/user"
DOOR_CLOSE_TOPIC = "aux/door/closed"


class MQTT:

    client: mqtt.Client
    _rfid_user_callback: Callable[[str], Any] | None
    _door_close_callback: Callable[[str], Any] | None

    def __init__(self):
        # Create client
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.connect(MQTT_BROKER_ADDRESS, port=MQTT_BROKER_PORT)

        # Add callback functions
        self.client.message_callback_add(RFID_USER_TOPIC, self._internal_rfid_user_callback)
        self.client.message_callback_add(DOOR_CLOSE_TOPIC, self._internal_door_closed_callback)

        # Subscribe to topics
        self.client.subscribe(RFID_USER_TOPIC)
        self.client.subscribe(DOOR_CLOSE_TOPIC)

        # Set all callback functions to None
        self._rfid_user_callback = None
        self._door_close_callback = None

    def _internal_rfid_user_callback(self, client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage):
        """
        Internal callback for the RFID_USER_TOPIC. Decodes MQTT message to get
        username and then calls function previously provided through
        set_rfid_user_callback()
        :param client:
        :param userdata:
        :param message:
        :return:
        """
        if self._rfid_user_callback is not None:
            self._rfid_user_callback(message.payload.decode("utf-8"))

    def _internal_door_closed_callback(self, client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage):
        """
        Internal callback for the DOOR_CLOSE_TOPIC
        :param client:
        :return:
        """
        if self._door_close_callback is not None:
            self._door_close_callback(message.payload.decode("utf-8"))

    def set_rfid_user_callback(self, callback: Callable[[str], Any]):
        """
        Set callback function for when a user is read with RFID
        :param callback: callback function. Should take uid (str) as an argument
        :return:
        """
        self._rfid_user_callback = callback

    def set_door_closed_callback(self, callback: Callable[[str], Any]):
        """
        Set callback function for when door is closed
        :param callback:
        :return:
        """
        self._door_close_callback = callback

    def start_listening(self):
        self.client.loop_start()

    def stop_listening(self):
        self.client.loop_stop()
