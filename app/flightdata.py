import configparser
import time
import logging
from threading import Thread

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.properties import DictProperty
from kivy.properties import NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup

from kivy.uix.progressbar import ProgressBar

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
logger.setLevel(level=logging.INFO)

# Create file handler and set level
file_handler = logging.FileHandler(filename=config.get("Paths", "base_path") + "/logs/flight_data_app.log",
                                   mode='w', encoding='utf-8')
file_handler.setLevel(level=logging.INFO)

# Create formatter
formatter = logging.Formatter(fmt="[%(levelname)s]\t%(asctime)s:\t%(message)s", datefmt='%Y-%m-%d %H:%M:%S')

# Add formatter to file handler
file_handler.setFormatter(fmt=formatter)

# Add file handler to logger
logger.addHandler(hdlr=file_handler)

# Window.fullscreen = 'auto'
Window.fullscreen = True
Window.maximize()


class HomeScreen(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.device_update, 0.5)
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

        self.thread = Thread(target=self.thread_upload, daemon=True)
        self.thread.start()

        label = Label(text='Uploading Please Wait', font_size=40, halign='center')
        progress_bar = ProgressBar(max=5)
        layout = GridLayout(rows=2)
        layout.add_widget(label)
        layout.add_widget(progress_bar)

        interim_popup = Popup(title='Uploading', size_hint=(None, None), size=(500, 400), content=layout)

        # interim_popup = InterimUploadPopup(title='Uploading')
        interim_popup.open()

        for i in range(5):
            progress_bar.value = i
            time.sleep(1)

        interim_popup.dismiss()

        # Open the post-transfer popup
        popup = UploadPopup(title='Upload Complete')
        popup.open()

        logger.info(f"Upload Completed: {time.time() - start_time} seconds")

    def thread_upload(self):
        try:
            # Transfer data from SD Card to Hard Drive
            data_manager.upload_flight_data()

        finally:
            self.thread = None

    def download_data(self):
        start_time = time.time()
        logger.debug('Download Pressed')

        # Open the post-transfer popup
        popup = PasswordPopup(title='Please Enter the PassKey')
        popup.open()

        logger.info(f"Download Completed: {time.time() - start_time}")


class InterimUploadPopup(Popup):

    def on_open(self):

        # Call dismiss_popup in 120 seconds
        Clock.schedule_once(self.dismiss, 120)


class UploadPopup(Popup):

    def on_open(self):
        Clock.schedule_interval(self.device_update, 1)

        # Call dismiss_popup in 60 seconds
        Clock.schedule_once(self.dismiss_popup, 60)

    def dismiss_popup(self, dt):
        device_manager.eject_sd()
        device_manager.eject_usb()
        self.dismiss()

    def device_update(self, dt):
        self.ids.copy_button.disabled = not device_manager.usb_status

    def copy_data(self):
        if data_manager.copy_sd_to_usb():

            # Erase sd card
            if clear_sd:
                data_manager.clear_sd_card()

            # Eject SD card
            device_manager.eject_sd()
            device_manager.eject_usb()

            self.dismiss()

    def exit_popup(self):
        # Erase sd card
        if clear_sd:
            data_manager.clear_sd_card()

        # Eject SD card
        device_manager.eject_sd()

        self.dismiss()


class CopyCompletePopup(Popup):
    def on_open(self):
        # Call dismiss_popup in 60 seconds
        Clock.schedule_once(self.dismiss_popup, 60)


class PasswordPopup(Popup):
    current_key = ''

    def on_open(self):
        # Call dismiss_popup in 60 seconds
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

    date_dict = DictProperty()
    usb_capacity = NumericProperty()

    def on_open(self):
        self.update_usb_capacity()
        self.update_directory_list()
        self.generate_buttons()

        # Call dismiss_popup in 60 seconds
        Clock.schedule_once(self.dismiss_popup, 60)

    def dismiss_popup(self, dt):
        self.dismiss()

    def update_usb_capacity(self):
        self.usb_capacity = device_manager.check_usb_capacity()

    def update_directory_list(self):
        self.date_dict = data_manager.parse_hd_dates()

    def generate_buttons(self):

        for key in self.date_dict.keys():
            btn = Button(text=f"{key}\n{self.date_dict[key]['size']} Mb", font_size=25, on_release=self.btn_press,
                         halign='center')
            if self.date_dict[key]['size'] > self.usb_capacity:
                btn.disabled = True
            self.ids.btn_grid.add_widget(btn)

        btn = Button(text='By Aircraft', font_size=25, on_release=self.btn_press, halign='center')
        self.ids.btn_grid.add_widget(btn)

    def btn_press(self, instance):
        selection = instance.text.split('\n')[0]

        for key in self.date_dict.keys():
            if selection == key:
                interim_popup = InterimDownloadPopup(title='Downloading')
                interim_popup.open()
                data_manager.download_flight_data(directories=self.date_dict[key]['dir_list'])
                time.sleep(3)
                interim_popup.dismiss()
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

        # Call dismiss_popup in 60 seconds
        Clock.schedule_once(self.dismiss_popup, 60)

    def dismiss_popup(self, dt):
        self.dismiss()

    def update_usb_capacity(self):
        self.usb_capacity = device_manager.check_usb_capacity()

    def update_aircraft_dict(self):
        self.aircraft_dict = data_manager.parse_hd_aircraft()

    def generate_buttons(self):

        layout = GridLayout(cols=4, spacing=10, size_hint=(1, None))
        layout.bind(minimum_height=layout.setter('height'))
        for key in self.aircraft_dict.keys():
            btn = Button(text=f"{key.split('-')[0]}\n{key.split('-')[1]}\n{self.aircraft_dict[key]['size']} Mb",
                         font_size=20, size_hint_y=None, height=100, on_release=self.btn_press, halign='center')
            layout.add_widget(btn)
        self.ids.scroll_view.add_widget(layout)

    def btn_press(self, instance):
        selection = "{}-{}".format(instance.text.split('\n')[0], instance.text.split('\n')[1])

        for key in self.aircraft_dict.keys():
            if selection == key:
                interim_popup = InterimDownloadPopup(title='Downloading')
                interim_popup.open()
                data_manager.download_flight_data(directories=self.aircraft_dict[key]['dir_list'])
                time.sleep(3)
                interim_popup.dismiss()
                popup = DownloadCompletePopup(title="Download Complete")
                popup.open()
                self.dismiss()


class InterimDownloadPopup(Popup):
    def on_open(self):

        # Call dismiss_popup in 120 seconds
        Clock.schedule_once(self.dismiss, 120)


class DownloadCompletePopup(Popup):

    def on_open(self):
        Clock.schedule_once(self.eject_usb, 3)

        # Call dismiss_popup in 60 seconds
        Clock.schedule_once(self.dismiss_popup, 60)

    def eject_usb(self, dt):
        device_manager.eject_usb()

    def dismiss_popup(self, dt):
        self.dismiss()


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
        Clock.schedule_once(self.initial_cap_update, 10)
        Clock.schedule_interval(self.update_capacity, 60)

    def initial_cap_update(self, dt):
        try:
            self.remaining_storage = str(device_manager.update_hd_capacity() // 1024)
            self.text = ' ' + self.remaining_storage + ' Gb Remaining'
            logger.debug(f"Hard drive remaining capacity updated: {self.remaining_storage} GiB")
        except Exception as e:
            logger.error(f"Initial HD cap update error: {e}")

    def update_capacity(self, dt):
        self.remaining_storage = str(device_manager.update_hd_capacity() // 1024)
        self.text = ' ' + self.remaining_storage + ' Gb Remaining'
        logger.debug(f"Hard drive remaining capacity updated: {self.remaining_storage} GiB")


class FlightDataApp(App):
    # Window.size = (800, 480)  # RPi 7 inch touchscreen (For Testing)
    pass


if __name__ == '__main__':
    FlightDataApp().run()
