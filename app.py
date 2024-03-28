from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard

from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window

class MemberCard(MDCard):
    name = StringProperty()
    job_title = StringProperty()
    major = StringProperty()

class MainApp(MDApp):
    def build(self):
        Window.size = (1024,600)
        
        self.root = BoxLayout()

        self.root.add_widget(Builder.load_file('app.kv'))

        print(self.root.ids)

        self.root.add_widget(
            MemberCard(name="Wilson", job_title="Cool guy", major="CS")
        )

if __name__ == "__main__":

    MainApp().run()