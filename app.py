import platform
import threading
from typing import List

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
from enum import Enum

RUNNING_ON_TARGET = False # Store if this is running on raspberry pi

# Check if this is running on Raspberry Pi
if platform.system() == "Linux" and "rpi" in platform.uname().release:
    RUNNING_ON_TARGET = True

class InfoScreen(MDScreen):
    pass



class CartScreen(Screen):
    cart_items = ListProperty([])

    def _refresh_cart(self):
        cart_view = self.children[1].children[1].children[0]
        cart_view.data = [{'title': item['title'], 'source': item['source'], 'price': item['price'], 'quantity': item['quantity']} for item in self.cart_items]
        cart_view.refresh_from_data()

    def add_item(self, item: models.Item, quantity: int):
        """
        Add an item to the
        :param item:
        :param quantity:
        :return:
        """
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
        for i in range(len(self.cart_items)):
            if self.cart_items[i].name == item.name:
                # This item is the one to remove
                new_quantity = self.cart_items[i].quantity - quantity_to_remove
                if new_quantity <= 0:
                    # Remove this item completely
                    self.cart_items.remove(i)
                else:
                    # Adjust the quantity of this item
                    self.cart_items[i].quantity = new_quantity
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


class States(Enum):
    WAITING_FOR_USER_TOKEN = 1
    CART_DOOR_OPEN = 2
    THANK_YOU = 3
    CANCEL_WAIT_FOR_DOOR_CLOSE = 4
    DEBUG = 5
    ABOUT = 6


class MainApp(MDApp):

    current_user: models.User = None
    state: States
    cart_screen: CartScreen | None

    def __init__(self, **kwargs):
        super().__init__()
        self.mqtt_client = None
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

    @mainthread
    def user_tap_callback(self, user):
        if self.current_user is None:
            self.current_user = user
            self.open_cart_screen()

    def open_cart_screen(self):
        """
        Open the cart screen
        :return:
        """
        self.cart_screen.empty_cart()
        self.root.children[0].transition.direction = 'left'
        self.root.children[0].current = 'Cart'
        # TODO open door
        self.state = States.CART_DOOR_OPEN

    def stop(self, *largs):
        self.mqtt_client.stop_listening()


if __name__ == "__main__":

    MainApp().run()
