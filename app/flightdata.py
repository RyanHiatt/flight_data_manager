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
from utils.devicemanager import DeviceManager

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

        # Check for SD Card
        self.ids.upload_button.disabled = not device_manager.check_for_device(device_manager.sd_device,
                                                                              device_manager.sd_path)
        # Check for USB Drive
        self.ids.download_button.disabled = not device_manager.check_for_device(device_manager.usb_device,
                                                                                device_manager.usb_path)


class DataTransferButton(Button):

    def upload_data(self):
        print('Upload Pressed')
        device_manager.unmount_device(device_manager.sd_path)

    def download_data(self):
        print('Download Pressed')
        device_manager.unmount_device(device_manager.usb_path)


class DataTransferLabel(Label):
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
    # Window.fullscreen = True


if __name__ == '__main__':
    FlightDataApp().run()
