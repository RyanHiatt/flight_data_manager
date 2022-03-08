import configparser
import time
import logging

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


# Instantiate configparser and read the config
config = configparser.ConfigParser()
config.read('config.ini')

# Instantiate the manager utils
data_manager = DataManager()
device_manager = DeviceManager()


# Instantiate logging
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.DEBUG)

# Create file handler and set level
file_handler = logging.FileHandler(filename=config.get("Paths", "base_path") + "/logs/flight_data_app.log",
                                   mode='w', encoding='utf-8')
file_handler.setLevel(level=logging.DEBUG)

# Create formatter
formatter = logging.Formatter(fmt="[%(levelname)s]\t%(asctime)s:\t%(message)s", datefmt='%Y-%m-%d %H:%M:%S')

# Add formatter to file handler
file_handler.setFormatter(fmt=formatter)

# Add file handler to logger
logger.addHandler(hdlr=file_handler)


class HomeScreen(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.device_update, 1)

    def device_update(self, dt):
        # Check for USB Drive and SD Card
        # usb_drive_status, sd_card_status = device_manager.check_for_devices()

        # self.ids.download_button.disabled = not usb_drive_status
        # self.ids.upload_button.disabled = not sd_card_status
        pass


class DataTransferButton(Button):

    def upload_data(self):
        start_time = time.time()
        logger.info('Upload Pressed')

        # Transfer data from SD Card to Hard Drive

        # Erase sd card
        if bool(config.get('Options', 'erase_sd')):
            data_manager.clear_sd_card()

        # Eject SD card
        device_manager.eject_sd()

        logger.info(f"Upload Completed: {time.time() - start_time}")

    def download_data(self):
        start_time = time.time()
        logger.info('Download Pressed')

        # Transfer data from Hard Drive to USB Drive

        # Eject USB Drive
        device_manager.eject_usb()

        logger.info(f"Download Completed: {time.time() - start_time}")


class DataTransferLabel(Label):
    pass


class OsuLogo(Image):
    pass


class VersionLabel(Label):
    app_version = StringProperty(config.get('Version', 'app_version'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = ' Version ' + self.app_version
        logger.info(f"Application version set: {self.app_version}")


class StorageLabel(Label):
    remaining_storage = StringProperty(config.get('Capacity', 'hd'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = ' ' + self.remaining_storage + ' Gb Remaining'
        Clock.schedule_interval(self.update_capacity, 60)

    def update_capacity(self, dt):
        self.remaining_storage = str(device_manager.update_hd_capacity())
        self.text = ' ' + self.remaining_storage + ' Gb Remaining'
        logger.debug(f"Hard drive remaining capacity updated: {self.remaining_storage}")


class FlightDataApp(App):
    Window.size = (800, 480)  # RPi 7 inch touchscreen (For Testing)
    pass


if __name__ == '__main__':
    FlightDataApp().run()
