import configparser

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import StringProperty

from utils.datamanager import DataManager
from utils.drivemanager import DriveManager

config = configparser.ConfigParser()
config.read('config.ini')

data_manager = DataManager(sd_dir=config.get('Paths', 'sd_dir'),
                           hd_dir=config.get('Paths', 'hd_dir'),
                           usb_dir=config.get('Paths', 'usb_dir'))
drive_manager = DriveManager()


class HomeScreen(GridLayout):
    pass


class DataTransferButton(Button):

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
