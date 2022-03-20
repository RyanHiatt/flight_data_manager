import psutil
import time
import os

import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def check_for_devices():
    devices = [device for device in psutil.disk_partitions()]

    for device in devices:
        print(device.device)
        if "sda" in device.device:
            hd_path = device.mountpoint
            print(f"Hard drive found: {hd_path}")

        if "sdb" in device.device:
            usb_path = device.mountpoint
            print(f"USB drive found: {usb_path}")

        if "mmcblk" in device.device and "0" not in device.device:
            sd_path = device.mountpoint
            print(f"SD card found: {sd_path}")


if __name__ == '__main__':
    nested_dict = {
        "one": {
            "a": "1a",
            "b": "1b"
        },
        "two": {
            "a": "2a",
            "b": "2b"
        },
        "three": {
            "a": "3a",
            "b": "3b"
        },
        "four": {
            "a": "4a",
            "b": "4b"
        },
    }

    print(nested_dict[1][1])