###############################################################################
#
# File: nfc_user_test.py
#
# Author: Isaac Ingram
#
# Purpose:
#
###############################################################################
import database
import utils.rfid_reader


def main():

    reader = utils.rfid_reader.RFIDReader()
    reader.start_read()

    while reader.waiting_for_card():
        print("Waiting for card")

    token = reader.get_last_read_value()

    user = database.get_user(user_token=token)

    print("Token belongs to user %s" % user.name)


if __name__ == '__main__':
    main()
