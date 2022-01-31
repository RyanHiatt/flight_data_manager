import os
import shutil
import configparser


class DriveManager:

    config = configparser.ConfigParser()
    config.read('../config.ini')

    def check_hd_capacity(self):
        total, used, free = shutil.disk_usage("/")

        print("Total: %d GiB" % (total // (2 ** 30)))
        print("Used: %d GiB" % (used // (2 ** 30)))
        print("Free: %d GiB" % (free // (2 ** 30)))


if __name__ == '__main__':
    manager = DriveManager()
    manager.check_hd_capacity()
