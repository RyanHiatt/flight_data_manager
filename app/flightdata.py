from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.window import Window

from utils.datamanager import DataManager


class HomeScreen(GridLayout):
    pass


class DataTransferButton(Button):
    pass


class DataTransferLabel(Label):
    pass


class SettingsButton(Button):
    pass


class OsuLogo(Image):
    pass


class VersionLabel(Label):
    pass


class FlightDataApp(App):
    Window.size = (800, 480)


if __name__ == '__main__':
    FlightDataApp().run()
