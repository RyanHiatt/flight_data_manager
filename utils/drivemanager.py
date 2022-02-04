import os
import shutil
import configparser

import pyudev
from pyudev._errors import DeviceNotFoundAtPathError


class DriveManager:

    # Instantiate config parser and read config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    context = pyudev.Context()

    # Drive Paths from config.ini
    sd_path = config.get('Paths', 'sd')
    hd_path = config.get('Paths', 'hd')
    usb_path = config.get('Paths', 'usb')

    sd_device = config.get('Devices', 'sd')
    hd_device = config.get('Devices', 'hd')
    usb_device = config.get('Devices', 'usb')

    def __init__(self):
        # Initialize DriveManager by updating remaining capacity
        # self.hd_remaining_cap = self.check_drive_capacity(self.hd_path)  # In GiB

        self.mount_device(self.hd_device, self.hd_path)

    @staticmethod
    def check_drive_capacity(drive):
        total, used, free = shutil.disk_usage(drive)

        print('Hard Drive Capacity Check:')
        print(f"\tTotal: {total // 1048576} MiB")
        print(f"\tUsed: {used // 1048576} MiB")
        print(f"\tFree: {free // 1048576} MiB")

        return free // 1048576

    def check_for_device(self, device, path):
        try:
            sd_device = pyudev.Devices.from_path(self.context, device)

            if sd_device in self.context.list_devices():
                self.mount_device(device, path)
                return True
            else:
                return False

        except DeviceNotFoundAtPathError:
            return False

    @staticmethod
    def mount_device(device, path):
        try:
            if os.path.ismount(path):
                pass
            else:
                os.system(f"mount {device} {path}")
                print(f"Device mounted at {path}")
        except PermissionError as e:
            print(f"Mounting error: {e}")

    @staticmethod
    def unmount_device(path):
        try:
            os.system(f'umount -l {path}')
            print(f"Device unmounted from {path}")
        except PermissionError as e:
            print(f"Mounting error: {e}")


if __name__ == '__main__':
    manager = DriveManager()
