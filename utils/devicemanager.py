import os
import shutil
import psutil
import configparser
import logging
from pathlib import Path

# Instantiate config parser and read config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Instantiate logging
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.DEBUG)

# Create file handler and set level
file_handler = logging.FileHandler(filename=config.get("Paths", "base_path") + "/logs/device_manager.log",
                                   mode='w', encoding='utf-8')
file_handler.setLevel(level=logging.DEBUG)

# Create formatter
formatter = logging.Formatter(fmt="[%(levelname)s]\t%(asctime)s:\t%(message)s", datefmt='%Y-%m-%d %H:%M:%S')

# Add formatter to file handler
file_handler.setFormatter(fmt=formatter)

# Add file handler to logger
logger.addHandler(hdlr=file_handler)


class DeviceManager:

    hd_status = False
    usb_status = False
    sd_status = False

    def __init__(self):
        # Initialize DriveManager
        self.locate_hd()
        self.update_hd_capacity()  # In GiB

    @staticmethod
    def check_device_capacity(path: str, name: str):
        total, used, free = shutil.disk_usage(path)

        logger.info(f"{name} Drive Capacity Check:\n"
                    f"\tTotal: {total // 1073741824} GiB\n"
                    f"\tUsed: {used // 1073741824} GiB\n"
                    f"\tFree: {free // 1073741824} GiB")

        return free // 1073741824  # In GiB

    @staticmethod
    def mount_device(device: str, path: str):  # Unused
        try:
            if os.path.ismount(path):
                pass
            else:
                os.system(f"sudo mount {device} {path}")
                if os.path.ismount(path):
                    logger.info(f"{device} mounted at {path}")
                    return True
                else:
                    logger.warning(f"Failed to mount: {device}")
                    return False
        except PermissionError as e:
            logger.error(f"Mounting error: {e}")
            pass

    @staticmethod
    def unmount_device(path: str):  # Unused
        try:
            os.system(f'sudo umount -l {path}')
            logger.info(f"Device unmounted from {path}")
            return True
        except PermissionError as e:
            logger.error(f"Mounting error: {e}")
            return False

    def update_hd_capacity(self):
        if self.hd_status:
            remaining_capacity = self.check_device_capacity(config.get('Paths', 'hd'), name='Hard Drive')

            config.set('Capacity', 'hd', str(remaining_capacity))
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            return remaining_capacity  # In GiB
        else:
            pass

    def check_usb_capacity(self):
        remaining_capacity = self.check_device_capacity(config.get('Paths', 'usb'), name='USB Drive')

        return remaining_capacity  # In GiB

    @staticmethod
    def make_mount_points():

        for device in ["hd", "usb", "sd"]:
            dev_path = config.get("Paths", "base_path") + "/mounts/" + device
            Path(dev_path).mkdir(parents=True, exist_ok=True)
            config.set("Paths", device, dev_path)
            logger.info(f"Mount point: {dev_path} created")

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def locate_hd(self):
        devices = [device for device in psutil.disk_partitions()]

        result = next((device for device in devices if config.get('Devices', 'hd') in device.device), False)

        if result:
            self.hd_status = True
            config.set('Paths', 'hd', result.mountpoint)
            logger.info(f"Hard drive found: {result.device}, location: {result.mountpoint}")

            with open('config.ini', 'w') as configfile:
                config.write(configfile)

        else:
            self.hd_status = False
            logger.warning("Hard drive not found")

        return self.hd_status

    def mount_hd(self, device: str):  # Unused
        return self.mount_device(device, config.get('Paths', 'hd'))

    @staticmethod
    def eject_hd():
        try:
            os.system(f"sudo umount -l {config.get('Paths', 'hd')}")
            logger.info(f"Device unmounted from {config.get('Paths', 'hd')}")
            return True
        except PermissionError as e:
            logger.error(f"Mounting error: {e}")
            return False

    def check_for_devices(self):
        devices = [device for device in psutil.disk_partitions()]

        usb_result = next((device for device in devices if config.get('Devices', 'usb') in device.device), False)
        sd_result = next((device for device in devices if config.get('Devices', 'sd') in device.device and
                          "0" not in device.device), False)

        if usb_result:
            if self.usb_status:
                pass
            else:
                self.usb_status = True
                config.set("Paths", "usb", usb_result.mountpoint)
                logger.info(f"USB drive found: {usb_result.device}")

                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
        else:
            if self.usb_status:
                self.eject_usb()
            else:
                logger.debug("USB drive not found")

        if sd_result:
            if self.sd_status:
                pass
            else:
                self.sd_status = True
                config.set("Paths", "sd", sd_result.mountpoint)
                logger.info(f"SD card found: {sd_result.device}")

                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
        else:
            if self.sd_status:
                self.eject_sd()
            else:
                logger.debug("SD card not found")

        return self.usb_status, self.sd_status

    # Unused
    def mount_usb(self, device: str):
        return self.mount_device(device, config.get('Paths', 'usb'))

    def eject_usb(self):
        try:
            path = config.get('Paths', 'usb')
            if path == "/":
                logger.error(f"Eject usb fail, path is '/'")
                self.sd_status = False
                return False
            else:
                os.system(f"sudo umount -l {path}")
                self.usb_status = False
                logger.debug(f"Device unmounted from {path}")
                return True
        except PermissionError as e:
            logger.error(f"USB ejection error: {e}")
            return False

    # Unused
    def mount_sd(self, device: str):
        return self.mount_device(device, config.get('Paths', 'sd'))

    def eject_sd(self):
        try:
            path = config.get('Paths', 'sd')
            if path == "/":
                logger.error(f"Eject sd fail, path is '/'")
                self.sd_status = False
                return False
            else:
                os.system(f"sudo umount -l {path}")
                self.sd_status = False
                logger.debug(f"Device unmounted from {path}")
                return True
        except PermissionError as e:
            logger.error(f"SD ejection error: {e}")
            return False


if __name__ == '__main__':
    manager = DeviceManager()

    usb_drive, sd_card = manager.check_for_devices()

    print(f"USB: {usb_drive}, SD: {sd_card}")
