import configparser

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

from utils.datamanager import DataManager
from utils.drivemanager import DriveManager

# Instantiate configparser and read the config
config = configparser.ConfigParser()
config.read('config.ini')

# Instantiate the manager utils
data_manager = DataManager()
drive_manager = DriveManager()


class HomeScreen(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.device_update, 2)

    def device_update(self, dt):

        self.ids.upload_button.disabled = not drive_manager.check_for_sd_card()
        self.ids.download_button.disabled = not drive_manager.check_for_usb_drive()


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
        super().__init__(**kwargs)
        self.text = ' Version ' + self.app_version


class FlightDataApp(App):
    Window.size = (800, 480)  # RPi 7 inch touchscreen (For Testing)


if __name__ == '__main__':
    FlightDataApp().run()
