from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout

from kivy.lang import Builder
from kivy.config import Config

class MainApp(MDApp):
    def build(self):

        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'width', '1024')
        Config.set('graphics', 'height', '600')
        
        self.root = BoxLayout()

        self.root.add_widget(Builder.load_file('app.kv'))

if __name__ == "__main__":

    MainApp().run()