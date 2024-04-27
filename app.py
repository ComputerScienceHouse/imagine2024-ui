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

RUNNING_ON_TARGET = False # Store if this is running on raspberry pi

# Check if this is running on Raspberry Pi
if platform.system() == "Linux" and "rpi" in platform.uname().release:
    RUNNING_ON_TARGET = True

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

class DebugScreen(MDScreen):
    def open_door(self):
        print("Opening door")
        pass

class CartItem(MDListItem):
    title = StringProperty()
    source = StringProperty()
    price = StringProperty()
    quantity = StringProperty()


class ImageButton(Widget):
    source = StringProperty()
    text = StringProperty()


class ShelfItem(BoxLayout):
    col = NumericProperty()
    row = NumericProperty()
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = f"Col: {self.col}  Row: {self.row}"
        self.size_hint = (None, None)
        self.size = ("120dp", "120dp")

    def calibrate(self):
        pass

class MemberCard(MDCard):
    name = StringProperty()
    job_title = StringProperty()
    major = StringProperty()


class MainApp(MDApp):

    current_user: models.User = None

    def __init__(self, **kwargs):
        super().__init__()
        self.mqtt_client = None



    def build(self):
        Window.size = (800,480)
        if RUNNING_ON_TARGET:
            Window.show_cursor = False

        # Set default loading image
        Loader.loading_image = Image('./images/item_placeholder.png')
        
        self.root = BoxLayout()

        self.root.add_widget(Builder.load_file('app.kv'))

        self.root.children[0].current = 'Start'

        self.mqtt_client = MQTT()
        self.mqtt_client.start_listening()

        self.mqtt_client.set_rfid_user_callback(self.user_tap_callback)

    @mainthread
    def user_tap_callback(self, user):
        if self.current_user is None:
            self.current_user = user
            self.root.children[0].transition.direction = 'left'
            self.root.children[0].current = 'Cart'

    def stop(self, *largs):
        self.mqtt_client.stop_listening()


if __name__ == "__main__":

    MainApp().run()
