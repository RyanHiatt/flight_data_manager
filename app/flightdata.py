import configparser
import time
import logging

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.properties import DictProperty
from kivy.properties import NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup

from utils.datamanager import DataManager
from utils.devicemanager import DeviceManager


# Instantiate configparser and read the config
config = configparser.ConfigParser()
config.read('config.ini')
clear_sd = bool(int(config.get('Options', 'erase_sd')))

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

Window.fullscreen = 'auto'


class HomeScreen(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.device_update, 1)
        logger.info("Device update loop initialized")

    def device_update(self, dt):
        # Check for USB Drive and SD Card
        usb_drive_status, sd_card_status = device_manager.check_for_devices()

        # Set the interface button disabled status
        self.ids.download_button.disabled = not usb_drive_status
        self.ids.upload_button.disabled = not sd_card_status


class DataTransferButton(Button):

    def upload_data(self):
        start_time = time.time()
        logger.debug('Upload Pressed')

        # Transfer data from SD Card to Hard Drive
        data_manager.upload_flight_data()

        # Open the post-transfer popup
        popup = UploadPopup(title='Upload Complete')
        popup.open()

        logger.info(f"Upload Completed: {time.time() - start_time} seconds")

    def download_data(self):
        start_time = time.time()
        logger.debug('Download Pressed')

        # Open the post-transfer popup
        popup = PasswordPopup(title='Please Enter the PassKey')
        popup.open()

        logger.info(f"Download Completed: {time.time() - start_time}")


class UploadPopup(Popup):

    def __init__(self, **kwargs):
        super(UploadPopup, self).__init__(**kwargs)
        Clock.schedule_interval(self.device_update, 1)

    def device_update(self, dt):
        self.ids.copy_button.disabled = not device_manager.usb_status

    def copy_data(self):
        if data_manager.copy_sd_to_usb():

            # Erase sd card
            if clear_sd:
                data_manager.clear_sd_card()

            # Eject SD card
            device_manager.eject_sd()

            self.dismiss()

    def exit_popup(self):
        # Erase sd card
        if clear_sd:
            data_manager.clear_sd_card()

        # Eject SD card
        device_manager.eject_sd()

        self.dismiss()


class PasswordPopup(Popup):
    current_key = ''

    def __init__(self, **kwargs):
        super(PasswordPopup, self).__init__(**kwargs)
        # call dismiss_popup in 60 seconds
        Clock.schedule_once(self.dismiss_popup, 60)

    def dismiss_popup(self, dt):
        self.dismiss()

    def btn_press(self, instance):
        self.current_key += str(instance.text)
        self.ids.passkey.text = self.ids.passkey.text + '*'
        self.ids.nope_label.text = ''

    def clear_text(self):
        self.ids.passkey.text = ''
        self.current_key = ''
        self.ids.nope_label.text = ''

    def submit(self):
        if self.current_key == config.get('Encryption', 'passkey'):
            self.clear_text()
            popup = DateSelectionPopup(title="Select Date Criteria")
            popup.open()

            self.dismiss()

        # If the key is incorrect, the else statement runs
        else:
            self.ids.passkey.text = ''
            self.current_key = ''
            self.ids.nope_label.text = 'Invalid Pass Key!'


class DateSelectionPopup(Popup):

    date_list = DictProperty()
    usb_capacity = NumericProperty()

    def on_open(self):
        self.update_usb_capacity()
        self.update_directory_list()
        self.update_buttons()

    def update_usb_capacity(self):
        self.usb_capacity = device_manager.check_usb_capacity()

    def update_directory_list(self):
        self.date_list = data_manager.parse_hd_dates()

    def update_buttons(self):
        self.ids.btn0.text = f"{self.date_list['Past Day']}\n{self.date_list['Past Day']['size']}"
        if self.date_list['Past Day']['size'] > self.usb_capacity:
            self.ids.btn0.disabled = True

        self.ids.btn1.text = f"{self.date_list['Past Week']}\n{self.date_list['Past Week']['size']}"
        if self.date_list['Past Week']['size'] > self.usb_capacity:
            self.ids.btn1.disabled = True

        self.ids.btn2.text = f"{self.date_list['Past Month']}\n{self.date_list['Past Month']['size']}"
        if self.date_list['Past Month']['size'] > self.usb_capacity:
            self.ids.btn2.disabled = True

        self.ids.btn3.text = f"{self.date_list['Past 3 Months']}\n{self.date_list['Past 3 Months']['size']}"
        if self.date_list['Past 3 Months']['size'] > self.usb_capacity:
            self.ids.btn3.disabled = True

        self.ids.btn4.text = f"{self.date_list['Past 6 Months']}\n{self.date_list['Past 6 Months']['size']}"
        if self.date_list['Past 6 Months']['size'] > self.usb_capacity:
            self.ids.btn4.disabled = True

        self.ids.btn5.text = f"{self.date_list['Past Year']}\n{self.date_list['Past Year']['size']}"
        if self.date_list['Past Year']['size'] > self.usb_capacity:
            self.ids.btn5.disabled = True

        self.ids.btn6.text = f"{self.date_list['All']}\n{self.date_list['All']['size']}"
        if self.date_list['All']['size'] > self.usb_capacity:
            self.ids.btn6.disabled = True

    def btn_press(self, instance):
        selection = instance.text

        for i in self.date_list.items():
            if selection == self.date_list[i]:
                data_manager.download_flight_data(directories=self.date_list[i][0])
                popup = DownloadCompletePopup(title="Download Complete")
                popup.open()
                self.dismiss()

        if selection == "By Aircraft":
            popup = AircraftSelectionPopup(title="Select Aircraft Criteria")
            popup.open()
            self.dismiss()


class AircraftSelectionPopup(Popup):

    aircraft_dict = DictProperty()
    usb_capacity = NumericProperty()

    def on_open(self):
        self.update_usb_capacity()
        self.update_aircraft_dict()
        self.generate_buttons()

    def update_usb_capacity(self):
        self.usb_capacity = device_manager.check_usb_capacity()

    def update_aircraft_dict(self):
        self.aircraft_dict = data_manager.parse_hd_aircraft()

    def generate_buttons(self):

        layout = StackLayout(cols=4, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(len(self.aircraft_dict)):
            btn = Button(text=f"{self.aircraft_dict[i]}\n{self.aircraft_dict[i][1]}",
                         size_hint_y=None, height=40)
            btn.bind(on_release=self.btn_press)
            layout.add_widget()
        self.ids.scroll_view.add_widget(layout)

    def btn_press(self, instance):
        selection = instance.text

        for i in range(len(self.aircraft_dict)):
            if selection == self.aircraft_dict[i]:
                data_manager.download_flight_data(directories=self.aircraft_list[i][0])
                popup = DownloadCompletePopup(title="Download Complete")
                popup.open()
                self.dismiss()


class DownloadCompletePopup(Popup):
    # Simple confirmation popup
    pass


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
    remaining_storage = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initial_cap_update()
        Clock.schedule_interval(self.update_capacity, 60)

    def initial_cap_update(self):
        self.remaining_storage = str(device_manager.update_hd_capacity() // 1024)
        self.text = ' ' + self.remaining_storage + ' Gb Remaining'
        logger.debug(f"Hard drive remaining capacity updated: {self.remaining_storage} GiB")

    def update_capacity(self, dt):
        self.remaining_storage = str(device_manager.update_hd_capacity() // 1024)
        self.text = ' ' + self.remaining_storage + ' Gb Remaining'
        logger.debug(f"Hard drive remaining capacity updated: {self.remaining_storage} GiB")


class FlightDataApp(App):
    # Window.size = (800, 480)  # RPi 7 inch touchscreen (For Testing)
    pass


if __name__ == '__main__':
    FlightDataApp().run()
