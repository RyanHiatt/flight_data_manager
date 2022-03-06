import configparser
import time

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

from utils.datamanager import DataManager
from utils.devicemanager import DeviceManager

Window.fullscreen = True

# Instantiate configparser and read the config
config = configparser.ConfigParser()
config.read('config.ini')

# Instantiate the manager utils
data_manager = DataManager()
device_manager = DeviceManager()


class HomeScreen(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.device_update, 1)

    def device_update(self, dt):
        # Check for USB Drive and SD Card
        usb_status, sd_card_status = device_manager.check_for_devices()

        self.ids.download_button.disabled = not usb_status
        self.ids.upload_button.disabled = not sd_card_status


class DataTransferButton(Button):

    def upload_data(self):
        start_time = time.time()
        print('Upload Pressed')

        # Transfer data from SD Card to Hard Drive

        # Eject SD card
        device_manager.eject_sd()

        print(f"Upload Completed: {time.time() - start_time}")

    def download_data(self):
        start_time = time.time()
        print('Download Pressed')

        # Transfer data from Hard Drive to USB Drive

        # Eject USB Drive
        device_manager.eject_usb()

        print(f"Download Completed: {time.time() - start_time}")


class DataTransferLabel(Label):
    pass


class OsuLogo(Image):
    pass


class VersionLabel(Label):
    app_version = StringProperty(config.get('Version', 'app_version'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = ' Version ' + self.app_version


class StorageLabel(Label):
    remaining_storage = StringProperty(config.get('Capacity', 'hd'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = ' ' + self.remaining_storage + ' Gb Remaining'
        Clock.schedule_interval(self.update_capacity, 60)

    def update_capacity(self, dt):
        self.remaining_storage = device_manager.update_hd_capacity()
        self.text = ' ' + self.remaining_storage + ' Gb Remaining'


class FlightDataApp(App):
    # Window.size = (800, 480)  # RPi 7 inch touchscreen (For Testing)
    pass


if __name__ == '__main__':
    FlightDataApp().run()
