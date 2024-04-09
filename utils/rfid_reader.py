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
import threading
from typing import Any

USE_RFID = False

# Check if the NFC reader can be used at all
if platform.system() == "Linux" and "rpi" in platform.uname().release:
    USE_RFID = True
    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522


class RFIDReader:

    # reader: SimpleMFRC522 | None
    read_thread: threading.Thread | None
    _done_reading_flag: bool
    last_card_value: Any

    def __init__(self):
        """
        Initialize this RFID reader
        """
        self.read_thread = None
        self.last_card_value = None
        self._done_reading_flag = False
        if USE_RFID:
            self.reader = SimpleMFRC522()
        else:
            self.reader = None

    def _read_card(self):
        """
        Function responsible for reading the RFID card. This should be the
        target function of the thread.
        :return:
        """
        self.last_card_value = self.reader.read_id()
        self._done_reading_flag = True

    def start_read(self) -> None:
        """
        Start looking for cards. This just signals the thread to
        begin reading cards.
        :return: None
        """
        if USE_RFID:
            # Spawn a read thread
            self.read_thread = threading.Thread(target=self._read_card)
            self.read_thread.start()

    def waiting_for_card(self) -> bool:
        """
        Check if the reader is waiting for a card. Will return True if the
        reader is running and waiting for a card. Once a card is read or the
        stop_read() function is called, this function will return False.
        :return: True if the reader is waiting on a card, False otherwise
        """
        if USE_RFID:
            if not self._done_reading_flag:
                # Not done reading, return True
                return True
            else:
                # Finished reading, return False
                self._done_reading_flag = False
                return False
        else:
            return False
            pass

    def get_last_read_value(self):
        """
        Get the value of the card that was last read
        :return:
        """
        return self.last_card_value
