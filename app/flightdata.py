import configparser
import threading

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty

from utils.datamanager import DataManager
from utils.drivemanager import DriveManager

# Instantiate configparser and read the config
config = configparser.ConfigParser()
config.read('config.ini')

# Instantiate the manager utils
data_manager = DataManager()
drive_manager = DriveManager()


class HomeScreen(GridLayout):
    pass


class DataTransferButton(Button):

    upload_enabled = drive_manager.sd_mounted
    download_enabled = drive_manager.usb_mounted

    def drive_check(self):
        print('check')

    def upload_data(self):
        print('Upload Pressed')

    def download_data(self):
        print('Download Pressed')


class DataTransferLabel(Label):
    pass


class SettingsButton(Button):
    pass


class OsuLogo(Image):
    pass


class VersionLabel(Label):
    app_version = StringProperty(config.get('Version', 'app_version'))

    def __init__(self, **kwargs):
        super(VersionLabel, self).__init__(**kwargs)
        self.text = ' Version ' + self.app_version


class FlightDataApp(App):
    Window.size = (800, 480)  # RPi 7 inch touchscreen (For Testing)


if __name__ == '__main__':
    FlightDataApp().run()
