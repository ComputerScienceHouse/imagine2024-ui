from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.list.list import MDListItem

from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget

class InfoScreen(MDScreen):
    pass

class CartScreen(MDScreen):
    pass

class StartScreen(MDScreen):
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
        
        self.root = BoxLayout()

        self.root.add_widget(Builder.load_file('app.kv'))

        self.root.children[0].current = 'Start'

if __name__ == "__main__":

    MainApp().run()