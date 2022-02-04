import os
import shutil
import configparser
import time

import pyudev
from pyudev._errors import DeviceNotFoundAtPathError


class DriveManager:

    # Instantiate config parser and read config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    context = pyudev.Context()

    # Drive Paths from config.ini
    sd_path = config.get('Paths', 'sd_dir')
    hd_path = config.get('Paths', 'hd_dir')
    usb_path = config.get('Paths', 'usb_dir')

    # def __init__(self):
    #     # Initialize DriveManager by updating remaining capacity
    #     self.hd_remaining_cap = self.check_drive_capacity(self.hd)  # In GiB

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
            sd_device = pyudev.Devices.from_path(context=self.context,
                                                 path=self.config.get('Devices', 'sd'))

            if sd_device in self.context.list_devices():
                return True
            else:
                return False

        except DeviceNotFoundAtPathError:
            return False

    def check_for_usb_drive(self):
        try:
            usb_device = pyudev.Devices.from_path(context=self.context,
                                                 path=self.config.get('Devices', 'usb'))

            if usb_device in self.context.list_devices():
                return True
            else:
                return False

        except DeviceNotFoundAtPathError:
            return False

    def check_for_hard_drive(self):
        try:
            hd_device = pyudev.Devices.from_path(context=self.context,
                                                 path=self.config.get('Devices', 'hd'))

            if hd_device in self.context.list_devices():
                return True
            else:
                return False

        except DeviceNotFoundAtPathError:
            return False


if __name__ == '__main__':
    manager = DriveManager()
