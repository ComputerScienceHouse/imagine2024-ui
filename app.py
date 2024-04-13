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
import utils.rfid_reader


class InfoScreen(MDScreen):
    pass


class CartScreen(Screen):
    cart_items = ListProperty([])

    def refresh_cart(self):
        cart_view = self.children[1].children[0]
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
        Window.size = (1024,600)

        # Set default loading image
        Loader.loading_image = Image('./images/item_placeholder.png')
        
        self.root = BoxLayout()

        self.root.add_widget(Builder.load_file('app.kv'))

        cart_screen = self.root.children[0].get_screen('Cart')
        cart_screen.cart_items = [
            {'title': 'Jolt Soda', 'source': 'images/oof.png', 'price': '3.00', 'quantity': '3'},
            {'title': 'Coffee', 'source': 'images/oof.png', 'price': '2.50', 'quantity': '2'},
            {'title': 'Tea', 'source': 'images/oof.png', 'price': '1.75', 'quantity': '5'},
            {'title': 'Orange Juice', 'source': 'images/oof.png', 'price': '4.50', 'quantity': '7'},
            {'title': 'Water', 'source': 'images/oof.png', 'price': '1.00', 'quantity': '4'},
            {'title': 'Smoothie', 'source': 'images/oof.png', 'price': '5.25', 'quantity': '6'},
            {'title': 'Milkshake', 'source': 'images/oof.png', 'price': '3.75', 'quantity': '9'},
            {'title': 'Lemonade', 'source': 'images/oof.png', 'price': '2.25', 'quantity': '8'},
            {'title': 'Iced Tea', 'source': 'images/oof.png', 'price': '2.00', 'quantity': '1'}
        ]
        cart_screen.refresh_cart()


if __name__ == "__main__":

    MainApp().run()
