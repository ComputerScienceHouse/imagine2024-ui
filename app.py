import json
import platform
import threading
from typing import List, Dict

from kivy.clock import mainthread
from kivy.core.image import Image
from kivy.loader import Loader
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.list.list import MDListItem

from kivy.properties import StringProperty, ListProperty
import models
from utils.mqtt import MQTT
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
import database
import models
import rfid_reader

RUNNING_ON_TARGET = False # Store if this is running on raspberry pi

# Check if this is running on Raspberry Pi
if platform.system() == "Linux" and "rpi" in platform.uname().release:
    RUNNING_ON_TARGET = True

MOCK_ITEM = models.Item(1, "Swedish Fish", 11111, 3.19, 5, 266, 10, 'http://placehold.jp/150x150.png', 'pouch')


class InfoScreen(MDScreen):
    pass



class CartScreen(Screen):
    cart_items = ListProperty([])

    def add_item(self, item: models.Item, quantity: int):
        """
        Add an item to the
        :param item:
        :param quantity:
        :return:
        """
        item_to_add = {'title': str(item.name), 'source': str(item.thumbnail_url), 'price': str(item.price), 'quantity': str(quantity)}
        self.cart_items.insert(0, item_to_add)

    def refresh_cart(self):
        cart_view = self.children[1].children[1].children[0]
        cart_view.data = [{'title': item['title'], 'source': item['source'], 'price': item['price'], 'quantity': item['quantity']} for item in self.cart_items]
        cart_view.refresh_from_data()


class StartScreen(MDScreen):
    pass


class AttractScreen(MDScreen):
    pass


class CartItem(MDListItem):
    title = StringProperty()
    source = StringProperty()
    price = StringProperty()
    quantity = StringProperty()


class ImageButton(Widget):
    source = StringProperty()
    text = StringProperty()


class MemberCard(MDCard):
    name = StringProperty()
    job_title = StringProperty()
    major = StringProperty()


class MainApp(MDApp):

    current_user: models.User = None
    connected_shelves: Dict[str, models.Shelf]

    def __init__(self, **kwargs):
        super().__init__()
        self.mqtt_client = None
        self.connected_shelves = None

    def build(self):
        Window.size = (800,480)
        if RUNNING_ON_TARGET:
            Window.show_cursor = False

        # Set default loading image
        Loader.loading_image = Image('./images/item_placeholder.png')

        item = models.Item(1, 'test', '', 3, 20, 226, 10, '', '')
        shelf = models.Shelf()
        self.slot = models.Slot(shelf, item)
        self.slot.set_conversion_factor(0.223)
        
        self.root = BoxLayout()

        self.root.add_widget(Builder.load_file('app.kv'))

        self.root.children[0].current = 'Start'

        self.mqtt_client = MQTT()
        self.mqtt_client.start_listening()

        self.mqtt_client.set_rfid_user_callback(self.user_tap_callback)
        self.mqtt_client.set_shelf_data_callback(self.shelf_data_callback)

    @mainthread
    def user_tap_callback(self, user):
        if self.current_user is None:
            self.current_user = user
            self.root.children[0].transition.direction = 'left'
            self.root.children[0].current = 'Cart'

    @mainthread
    def shelf_data_callback(self, data_string):
        """
        Callback function for when data is received for a shelf via MQTT
        :param data_string: The data string, directly from MQTT
        :return:
        """
        try:
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
                # Shelf already exists
                self.connected_shelves[shelf_id].update(slot_values)
            else:
                # Shelf does not exist
                # Create new shelf with items
                items_for_shelf = [MOCK_ITEM, MOCK_ITEM, MOCK_ITEM, MOCK_ITEM]
                self.connected_shelves[shelf_id] = models.Shelf(items_for_shelf)
                # Update weight values
                self.connected_shelves[shelf_id].update(slot_values)
        except KeyError as key_error:
            print("KeyError when parsing shelf data from MQTT")
            print(f"\tData: '{data_string}'")
            print(f"\tFull exception: {key_error}")
        except Exception as e:
            print("Exception occurred when reading shelf data from MQTT")
            print(f"Full exception: {e}")

    def stop(self, *largs):
        self.mqtt_client.stop_listening()


if __name__ == "__main__":

    MainApp().run()
