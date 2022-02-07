import os
import shutil
import configparser

import pyudev
from pyudev._errors import DeviceNotFoundAtPathError


class DeviceManager:

    # Instantiate config parser and read config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    context = pyudev.Context()

    # Drive paths from config.ini
    sd_path = config.get('Paths', 'sd')
    hd_path = config.get('Paths', 'hd')
    usb_path = config.get('Paths', 'usb')

    # Device names from config.ini
    sd_device = config.get('Devices', 'sd')
    hd_device = config.get('Devices', 'hd')
    usb_device = config.get('Devices', 'usb')

    def __init__(self):
        # Initialize DriveManager
        # self.hd_remaining_cap = self.check_drive_capacity(self.hd_path)  # In GiB
        self.check_mount_points()
        # self.mount_device(self.hd_device, self.hd_path)
        pass

    @staticmethod
    def check_drive_capacity(drive: str):
        total, used, free = shutil.disk_usage(drive)

        print(f"{drive} Capacity Check:")
        print(f"\tTotal: {total // 1048576} MiB")
        print(f"\tUsed: {used // 1048576} MiB")
        print(f"\tFree: {free // 1048576} MiB")

        return free // 1048576

    def check_mount_points(self):
        """

        :return:
        """
        # Check if SD Card mount point exists
        if os.path.exists(self.sd_path):
            pass
        else:  # Create SD Card mount point
            os.makedirs(self.sd_path)

        # Check if Hard Drive mount point exists
        if os.path.exists(self.hd_path):
            pass
        else:  # Create Hard Drive mount point
            os.makedirs(self.hd_path)

        # Check if USB Drive mount point exists
        if os.path.exists(self.usb_path):
            pass
        else:  # Create USB Drive mount point
            os.makedirs(self.usb_path)

    def check_for_device(self, device: str, path: str):

        try:
            target_device = pyudev.Devices.from_path(self.context, device)

            if target_device in self.context.list_devices():
                self.mount_device(target_device, device, path)
                print(f"Found: {target_device.sys_name}")
                return True
            else:
                return False

        except DeviceNotFoundAtPathError:
            return False

    @staticmethod
    def mount_device(target_device, device: str, path: str):
        try:
            if os.path.ismount(path):
                pass
            else:
                os.system(f"sudo mount {device} {path}")
                if os.path.ismount(path):
                    print(f"{target_device.sys_name} mounted at {path}")
                else:
                    print(f"Failed to mount: {target_device.sys_name}")
        except PermissionError as e:
            print(f"Mounting error: {e}")

    @staticmethod
    def unmount_device(path: str):
        try:
            os.system(f'umount -l {path}')
            print(f"Device unmounted from {path}")
        except PermissionError as e:
            print(f"Mounting error: {e}")


if __name__ == '__main__':
    manager = DeviceManager()
