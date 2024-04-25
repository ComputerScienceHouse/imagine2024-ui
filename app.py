import platform
from kivy.core.image import Image
from kivy.loader import Loader
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.list.list import MDListItem

from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget

import database
import models
import utils.rfid_reader

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
    def build(self):
        Window.size = (800,400)
        if RUNNING_ON_TARGET:
            Window.show_cursor = False

        # Set default loading image
        Loader.loading_image = Image('./images/item_placeholder.png')
        
        self.root = BoxLayout()

        self.root.add_widget(Builder.load_file('app.kv'))

        cart_screen = self.root.children[0].get_screen('Cart')
        cart_data = database.get_items()
        for data in cart_data:
            cart_screen.add_item(data, 2)
            cart_screen.refresh_cart()


if __name__ == "__main__":

    MainApp().run()
