import os
import shutil
import configparser


class DriveManager:

    # Instantiate config parser and read config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Drive Paths from config.ini
    hd = config.get('Drives', 'hd')
    usb = config.get('Drives', 'usb')
    sd = config.get('Drives', 'sd')

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
            return os.path.exists(self.sd)

    def check_for_usb_drive(self):
        return os.path.exists(self.usb)



if __name__ == '__main__':
    manager = DriveManager()
