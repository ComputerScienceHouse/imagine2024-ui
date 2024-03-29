from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen

from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window

class InfoScreen(MDScreen):
    pass

class CartScreen(MDScreen):
    pass

class StartScreen(MDScreen):
    pass

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