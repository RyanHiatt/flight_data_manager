import os
import shutil
import configparser
import time

import pyudev


class DriveManager:

    # Instantiate config parser and read config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    context = pyudev.Context()

    hd_device = pyudev.Devices.from_name(context, config.get('HD', 'subsystem'), config.get('HD', 'sys_name'))


    # Drive Paths from config.ini
    hd_path = config.get('Paths', 'hd')
    usb_path = config.get('Paths', 'usb')
    sd_path = config.get('Paths', 'sd')

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
        sd_device = pyudev.Devices.from_name(self.context,
                                             self.config.get('SD', 'subsystem'),
                                             self.config.get('SD', 'sys_name'))

        if sd_device in self.context.list_devices():
            return True
        else:
            return False

    def check_for_usb_drive(self):
        usb_device = pyudev.Devices.from_name(self.context,
                                              self.config.get('USB', 'subsystem'),
                                              self.config.get('USB', 'sys_name'))

        if usb_device in self.context.list_devices():
            return True
        else:
            return False

    def check_for_hard_drive(self):
        if self.hd_device in self.context.list_devices():
            return True
        else:
            return False


if __name__ == '__main__':
    manager = DriveManager()
