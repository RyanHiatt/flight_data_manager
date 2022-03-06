import os
import shutil
import psutil
import configparser
from pathlib import Path


class DeviceManager:

    # Instantiate config parser and read config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    hd_status = False
    usb_status = False
    sd_status = False

    def __init__(self):
        # Initialize DriveManager
        self.make_mount_points()
        self.locate_hd()
        self.check_for_devices()
        self.update_hd_capacity()  # In GiB

    @staticmethod
    def check_device_capacity(path, name):
        total, used, free = shutil.disk_usage(path)

        print(f"{name} Drive Capacity Check:")
        print(f"\tTotal: {total // 1073741824} GiB")
        print(f"\tUsed: {used // 1073741824} GiB")
        print(f"\tFree: {free // 1073741824} GiB")

        return free // 1073741824  # In GiB

    @staticmethod
    def mount_device(device, path: str):
        try:
            if os.path.ismount(path):
                pass
            else:
                os.system(f"sudo mount {device} {path}")
                if os.path.ismount(path):
                    print(f"{device} mounted at {path}")
                    return True
                else:
                    print(f"Failed to mount: {device.sys_name}")
                    return False
        except PermissionError as e:
            print(f"Mounting error: {e}")
            pass

    @staticmethod
    def unmount_device(path: str):
        try:
            os.system(f'sudo umount -l {path}')
            print(f"Device unmounted from {path}")
            return True
        except PermissionError as e:
            print(f"Mounting error: {e}")
            return False

    def update_hd_capacity(self):
        remaining_capacity = self.check_device_capacity(self.config.get('Paths', 'hd'), name='Hard Drive')

        self.config.set('Capacity', 'hd', str(remaining_capacity))
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        return remaining_capacity  # In GiB

    def check_usb_capacity(self):
        remaining_capacity = self.check_device_capacity(self.config.get('Paths', 'usb'), name='USB Drive')

        return remaining_capacity  # In GiB

    def make_mount_points(self):

        for device in ["hd", "usb", "sd"]:
            dev_path = self.config.get("Paths", "base_path") + "/mounts/" + device
            Path(dev_path).mkdir(parents=True, exist_ok=True)
            self.config.set("Paths", device, dev_path)

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def locate_hd(self):
        devices = [device for device in psutil.disk_partitions()]

        result = next((device for device in devices if self.config.get('Devices', 'hd') in device.device), False)
        print(result)
        if result:
            print("Hard drive found")
            if self.hd_status:
                pass
            else:
                if self.mount_hd(device=result.device):  # Mount the Hard Drive
                    self.hd_status = True
                    print("Hard drive mounted")
                else:
                    print("Failed to mount hard drive")
        else:
            self.hd_status = False
            print("Hard drive not found")

        return self.hd_status

    def mount_hd(self, device):
        return self.mount_device(device, self.config.get('Paths', 'hd'))

    def check_for_devices(self):
        devices = [device for device in psutil.disk_partitions()]

        usb_result = next((device for device in devices if self.config.get('Devices', 'usb') in device.device), False)
        sd_result = next((device for device in devices if self.config.get('Devices', 'sd') in device.device and "0" not in device.device), False)

        if usb_result:
            print("USB drive found")
            if self.usb_status:
                pass
            else:
                if self.mount_usb(device=usb_result.device):
                    self.usb_status = True
                    print("USB drive mounted")
                else:
                    print("USB drive failed to mount")
        else:
            self.eject_usb()
            self.usb_status = False
            print("USB drive not found")

        if sd_result:
            print("SD card found")
            if self.sd_status:
                pass
            else:
                if self.mount_sd(device=sd_result.device):
                    self.sd_status = True
                    print("SD card mounted")
                else:
                    print("sd card failed to mount")
        else:
            self.eject_sd()
            self.sd_status = False
            print("SD card not found")

        # for device in devices:
        #     if self.config.get('Devices', 'usb') in device.device:
        #         # Mount the USB Drive
        #         self.mount_usb(device=device.device)
        #         self.usb_status = True
        #         print("USB drive found")
        #
        #     if self.config.get('Devices', 'sd') in device.device and "0" not in device.device:
        #         # Mount the SD Card
        #         self.mount_sd(device=device.device)
        #         self.sd_status = True
        #         print("SD card found")

        return self.usb_status, self.sd_status

    def mount_usb(self, device):
        return self.mount_device(device, self.config.get('Paths', 'usb'))

    def eject_usb(self):
        try:
            os.system(f"sudo umount -l {self.config.get('Paths', 'usb')}")
            print(f"Device unmounted from {self.config.get('Paths', 'usb')}")
            return True
        except PermissionError as e:
            print(f"Mounting error: {e}")
            return False

    def mount_sd(self, device):
        return self.mount_device(device, self.config.get('Paths', 'sd'))

    def eject_sd(self):
        try:
            os.system(f"sudo umount -l {self.config.get('Paths', 'sd')}")
            print(f"Device unmounted from {self.config.get('Paths', 'sd')}")
            return True
        except PermissionError as e:
            print(f"Mounting error: {e}")
            return False


if __name__ == '__main__':
    manager = DeviceManager()

    usb_drive, sd_card = manager.check_for_devices()

    print(f"USB: {usb_drive}, SD: {sd_card}")
