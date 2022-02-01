import os
import shutil
import configparser
from threading import Thread
import time


class DriveManager:

    # Instantiate config parser and read config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Drive Paths from config.ini
    hd = config.get('Drives', 'hd')
    usb = config.get('Drives', 'usb')
    sd = config.get('Drives', 'sd')

    sd_mounted = False
    usb_mounted = False

    def __init__(self):
        # Initialize DriveManager by updating remaining capacity
        self.hd_remaining_cap = self.check_drive_capacity(self.hd)  # In GiB

    @staticmethod
    def check_drive_capacity(drive):
        total, used, free = shutil.disk_usage(drive)

        print('Hard Drive Capacity Check:')
        print(f"\tTotal: {total // 1048576} MiB")
        print(f"\tUsed: {used // 1048576} MiB")
        print(f"\tFree: {free // 1048576} MiB")

        return free // 1048576

    def check_for_sd_card(self):
        try:
            return os.path.exists(self.sd)
        except IOError or PermissionError or OSError as e:
            print(f"Existing Directory Error: {e}")

    def check_for_usb_drive(self):
        try:
            return os.path.exists(self.usb)
        except IOError or PermissionError or OSError as e:
            print(f"Existing Directory Error: {e}")

    def background_drive_checking(self):

        self.sd_mounted = self.check_for_sd_card()

        self.usb_mounted = self.check_for_usb_drive()

    def create_drive_check_thread(self):

        new_thread = Thread(target=self.background_drive_checking(), name='drive_checking', daemon=True)
        new_thread.start()

        while True:
            print(self.sd_mounted, self.usb_mounted)
            time.sleep(1)


if __name__ == '__main__':
    manager = DriveManager()
