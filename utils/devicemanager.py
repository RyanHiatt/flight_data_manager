import os
import shutil
import psutil
import configparser


class DeviceManager:

    # Instantiate config parser and read config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    def __init__(self):
        # Initialize DriveManager
        self.locate_hd()
        self.check_for_devices()
        self.update_hd_capacity()  # In GiB
        pass

    @staticmethod
    def check_device_capacity(path, name):
        total, used, free = shutil.disk_usage(path)

        print(f"{name} Drive Capacity Check:")
        print(f"\tTotal: {total // 1073741824} GiB")
        print(f"\tUsed: {used // 1073741824} GiB")
        print(f"\tFree: {free // 1073741824} GiB")

        return free // 1073741824  # In GiB

    def update_hd_capacity(self):
        remaining_capacity = self.check_device_capacity(self.config.get('Paths', 'hd'), name='Hard Drive')

        self.config.set('Capacity', 'hd', str(remaining_capacity))
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        return str(remaining_capacity)  # In GiB

    def check_usb_capacity(self):
        remaining_capacity = self.check_device_capacity(self.config.get('Paths', 'usb'), name='USB Drive')

        return remaining_capacity  # In GiB

    def locate_hd(self):
        devices = [device for device in psutil.disk_partitions()]

        hard_drive_status = False

        for device in devices:
            if self.config.get('Devices', 'hd') in device.device:
                self.config.set('Paths', 'hd', device.mountpoint)
                hard_drive_status = True
                print("Hard drive found")

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        return hard_drive_status

    def check_for_devices(self):
        devices = [device for device in psutil.disk_partitions()]

        usb_drive_status = False
        sd_card_status = False

        for device in devices:
            if self.config.get('Devices', 'usb') in device.device:
                self.config.set('Paths', 'usb', device.mountpoint)
                usb_drive_status = True
                print("USB drive found")

            if self.config.get('Devices', 'sd') in device.device and "0" not in device.device:
                self.config.set('Paths', 'sd', device.mountpoint)
                sd_card_status = True
                print("SD card found")

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        return usb_drive_status, sd_card_status

    def eject_usb(self):
        try:
            os.system(f"sudo umount -l {self.config.get('Paths', 'usb')}")
            print(f"Device unmounted from {self.config.get('Paths', 'usb')}")
            return True
        except PermissionError as e:
            print(f"Mounting error: {e}")
            return False

    def eject_sd(self):
        try:
            os.system(f"sudo umount -l {self.config.get('Paths', 'sd')}")
            print(f"Device unmounted from {self.config.get('Paths', 'sd')}")
            return True
        except PermissionError as e:
            print(f"Mounting error: {e}")
            return False

    @staticmethod
    def mount_device(device, path: str):
        try:
            if os.path.ismount(path):
                pass
            else:
                os.system(f"sudo mount {device} {path}")
                if os.path.ismount(path):
                    print(f"{device} mounted at {path}")
                else:
                    print(f"Failed to mount: {device.sys_name}")
        except PermissionError as e:
            print(f"Mounting error: {e}")

    @staticmethod
    def unmount_device(path: str):
        try:
            os.system(f'sudo umount -l {path}')
            print(f"Device unmounted from {path}")
        except PermissionError as e:
            print(f"Mounting error: {e}")


if __name__ == '__main__':
    manager = DeviceManager()

    usb_drive, sd_card = manager.check_for_devices()

    print(f"USB: {usb_drive}, SD: {sd_card}")
