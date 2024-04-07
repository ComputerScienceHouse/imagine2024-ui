from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.properties import DictProperty
from kivy.core.window import Window


class InfoScreen(MDScreen):
    pass

class InfoCard(MDCard):
    source = StringProperty()
    title = StringProperty()
    content = StringProperty()

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
        Window.show_cursor = False
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.accent_palette = "Orange"
        self.root = BoxLayout()

        self.root.add_widget(Builder.load_file('app.kv'))

        self.root.children[0].current = 'Info'


if __name__ == "__main__":

    MainApp().run()
