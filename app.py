import threading
from typing import List

from kivy.core.image import Image
from kivy.loader import Loader
from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.list.list import MDListItem
from utils.mqtt import MQTT
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget


class InfoScreen(MDScreen):
    pass


class CartScreen(MDScreen):
    pass


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
        Window.size = (1024,600)

        # Set default loading image
        Loader.loading_image = Image('./images/item_placeholder.png')
        
        self.root = BoxLayout()

        self.root.add_widget(Builder.load_file('app.kv'))

        self.root.children[0].current = 'Start'

        self.mqtt_client = MQTT()
        self.mqtt_client.start_listening()

        self.mqtt_client.set_rfid_user_callback(self.user_tap_callback)

    def user_tap_callback(self, user):
        self.root.children[0].transition.direction = 'right'
        self.root.children[0].current = 'Cart'

    def stop(self, *largs):
        self.mqtt_client.stop_listening()


if __name__ == "__main__":

    MainApp().run()
