import json
import math
import platform
import threading
from typing import List, Dict

from kivy.clock import mainthread, Clock
from kivy.core.image import Image
from kivy.loader import Loader
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.list.list import MDListItem

from kivy.properties import StringProperty, ListProperty, NumericProperty
import models
from utils.mqtt import MQTT
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
import database
import models
import rfid_reader
from enum import Enum

RUNNING_ON_TARGET = False # Store if this is running on raspberry pi

# Check if this is running on Raspberry Pi
if platform.system() == "Linux" and "rpi" in platform.uname().release:
    RUNNING_ON_TARGET = True

MOCK_ITEM = models.Item(1, "Swedish Fish", 11111, 3.19, 5, 266, 26, 'http://placehold.jp/150x150.png', 'pouch')
# HARDCODED SHELF DATA
# Shelf Address -> Slot number (list) -> Tuple (Item ID in database, division factor for weight)
SHELF_DATA = {
    '80:65:99:E3:8B:92': [(1, 0.26), (1, 0.26), (1, 0.26), (1, 0.26)],
    'id2': [(1, 0.26), (1, 0.26), (1, 0.26), (1, 0.26)],
    'id3': [(1, 0.26), (1, 0.26), (1, 0.26), (1, 0.26)],
    'id4': [(1, 0.26), (1, 0.26), (1, 0.26), (1, 0.26)]
}


class InfoScreen(MDScreen):
    pass


class CartScreen(Screen):
    cart_items = ListProperty([])

    def _refresh_cart(self):
        cart_view = self.children[0].children[1].children[0]
        cart_view.data = [{'title': item['title'], 'source': item['source'], 'price': item['price'], 'quantity': item['quantity']} for item in self.cart_items]
        cart_view.refresh_from_data()

    def add_item(self, item: models.Item, quantity: int):
        quantity = abs(quantity)
        print(f"NEW QUANTITY {quantity}")
        """
        Add an item to the
        :param item:
        :param quantity:
        :return:
        """
        # Check if this item is already in the cart
        for i in range(len(self.cart_items)):
            if self.cart_items[i]['title'] == item.name:
                # Item is already in the cart
                self.cart_items[i]['quantity'] = str(int(self.cart_items[i]['quantity']) + quantity)
                self._refresh_cart()
                return
        item_to_add = {'title': str(item.name), 'source': str(item.thumbnail_url), 'price': str(item.price), 'quantity': str(quantity)}
        self.cart_items.insert(0, item_to_add)
        self._refresh_cart()

    def remove_item(self, item: models.Item, quantity_to_remove: int):
        """
        Remove an item from the cart
        :param item: Item to remove
        :param quantity_to_remove: Quantity to remove
        :return:
        """
        quantity_to_remove = abs(quantity_to_remove)
        for i in range(len(self.cart_items)):
            if self.cart_items[i]['title'] == item.name:
                # This item is the one to remove
                new_quantity = int(self.cart_items[i]['quantity']) - quantity_to_remove
                if new_quantity <= 0:
                    # Remove this item completely
                    del self.cart_items[i]
                else:
                    # Adjust the quantity of this item
                    self.cart_items[i]['quantity'] = str(new_quantity)
                # Refresh view
                self._refresh_cart()
                return

    def empty_cart(self):
        """
        Empty the cart
        :return:
        """
        self.cart_items.clear()
        self._refresh_cart()


class StartScreen(MDScreen):
    pass

class AttractScreen(MDScreen):
    pass

class DebugScreen(MDScreen):
    def open_door(self):
        print("Opening door")
        pass

class CancelScreen(MDScreen):
    pass


class ThankYouScreen(MDScreen):
    pass


class CartItem(MDListItem):
    title = StringProperty()
    source = StringProperty()
    price = StringProperty()
    quantity = StringProperty()


class ImageButton(Widget):
    source = StringProperty()
    text = StringProperty()


class ShelfItem(Widget):
    shelf = NumericProperty()
    slot = NumericProperty()
    text = StringProperty()

    def on_shelf(self, instance, value):
        self.text = f"Shelf: {self.shelf}  Slot: {self.slot}"

    def on_slot(self, instance, value):
        self.text = f"Shelf: {self.shelf}  Slot: {self.slot}"

    def calibrate(self):
        pass

class MemberCard(MDCard):
    name = StringProperty()
    job_title = StringProperty()
    major = StringProperty()


class States(Enum):
    WAITING_FOR_USER_TOKEN = 1
    CART_DOOR_OPEN = 2
    THANK_YOU = 3
    CANCEL_WAIT_FOR_DOOR_CLOSE = 4
    DEBUG = 5
    ABOUT = 6


class MainApp(MDApp):

    connected_shelves: Dict[str, models.Shelf]
    current_user: models.User | None = None
    state: States
    cart_screen: CartScreen | None

    def __init__(self, **kwargs):
        super().__init__()
        self.mqtt_client = None
        self.connected_shelves = dict()
        self.state = States.WAITING_FOR_USER_TOKEN
        self.cart_screen = None

    def build(self):
        Window.size = (800,480)
        if RUNNING_ON_TARGET:
            Window.show_cursor = False

        # Set default loading image
        Loader.loading_image = Image('./images/item_placeholder.png')

        self.root = BoxLayout()

        self.root.add_widget(Builder.load_file('app.kv'))
        self.cart_screen: CartScreen = self.root.children[0].screens[1]

        self.root.children[0].current = 'Start'
        self.state = States.WAITING_FOR_USER_TOKEN

        self.mqtt_client = MQTT()
        self.mqtt_client.start_listening()

        self.mqtt_client.set_rfid_user_callback(self.user_tap_callback)
        self.mqtt_client.set_shelf_data_callback(self.shelf_data_callback)
        self.mqtt_client.set_door_closed_callback(self.door_closed_callback)

        # Read in all shelves
        for shelf_id in SHELF_DATA:
            items = list()
            conversion_factors = list()
            for item, conversion_factor in SHELF_DATA[shelf_id]:
                items.append(MOCK_ITEM)
                conversion_factors.append(conversion_factor)
            shelf = models.Shelf(items)
            for i in range(len(shelf.slots)):
                shelf.slots[i].set_conversion_factor(conversion_factors[i])
            self.connected_shelves[shelf_id] = shelf

    @mainthread
    def user_tap_callback(self, user_txt):
        if user_txt[:5] != "User[":
            return
        user_split = user_txt[5:].split(',')
        user = models.User(
            user_split[0],
            user_split[1],
            user_split[2],
            user_split[3][0:],
            user_split[4],
            user_split[5],
            user_split[6]
        )
        if self.state == States.WAITING_FOR_USER_TOKEN:
            if 'admin' in user.name:
                # Admin user
                self.root.children[0].transition.direction = 'right'
                self.root.children[0].current = 'Debug'
            else:
                self.current_user = user
                self.open_cart_screen()

    @mainthread
    def door_closed_callback(self, message):
        """
        Callback for when door closed message is received over MQTT
        :return:
        """
        if self.state == States.CANCEL_WAIT_FOR_DOOR_CLOSE:
            # Cancelled transaction waiting on door to close. Go to start screen
            self.go_to_start_screen()
        elif self.state == States.CART_DOOR_OPEN:
            # Active transaction signal end. Go to thank you screen, then go to cart screen
            self.root.children[0].transition.direction = 'left'
            self.root.children[0].current = 'ThankYou'
            Clock.schedule_once(self.go_to_start_screen(), 3)

    def go_to_start_screen(self):
        self.root.children[0].transition.direction = 'right'
        self.root.children[0].current = 'Start'
        self.current_user = None

    def open_cart_screen(self):
        """
        Open the cart screen
        :return:
        """
        self.cart_screen.empty_cart()
        self.root.children[0].transition.direction = 'left'
        self.root.children[0].current = 'Cart'
        self.mqtt_client.publish_doors_open()
        self.state = States.CART_DOOR_OPEN

    def open_door(self):
        self.mqtt_client.publish_doors_open()

    def cancel_transaction(self):
        """
        Cancel transaction
        :return:
        """
        self.state = States.CANCEL_WAIT_FOR_DOOR_CLOSE
        self.root.children[0].transition.direction = 'left'
        self.root.children[0].current = 'Cancel'

    @mainthread
    def shelf_data_callback(self, data_string):
        """
        Callback function for when data is received for a shelf via MQTT
        :param data_string: The data string, directly from MQTT
        :return:
        """
        #try:
        # Deconstruct JSON data
        data = json.loads(data_string)
        print(data)
        shelf_id = data['id']
        slot_values = data['data']
        send_time_millis = data['time']

        # Check that slot values are a list
        if not isinstance(slot_values, list):
            raise Exception("IncorrectFormat: Slot values incorrect format (not list)")
        if shelf_id in self.connected_shelves:
            adjustments = self.connected_shelves[shelf_id].update(slot_values)
            for item, quantity_adjust in adjustments:
                if quantity_adjust < 0:
                    self.cart_screen.add_item(item, quantity_adjust)
                    print("ADD ITEM TO CART")
                elif quantity_adjust > 0:
                    self.cart_screen.remove_item(item, quantity_adjust)
                    print("REMOVE ITEM FROM CART")

        # except KeyError as key_error:
        #     print("KeyError when parsing shelf data from MQTT")
        #     print(f"\tData: '{data_string}'")
        #     print(f"\tFull exception: {key_error}")
        # except Exception as e:
        #     print("Exception occurred when reading shelf data from MQTT")
        #     print(f"Full exception: {e}")

    def stop(self, *largs):
        self.mqtt_client.stop_listening()


if __name__ == "__main__":

    MainApp().run()
