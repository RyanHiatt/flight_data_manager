import os
import shutil
import configparser
import filecmp
import secrets


from utils.exceptions import MismatchFileError


class DataManager:
    config = configparser.ConfigParser()
    config.read('config.ini')

    def __init__(self, sd_dir, hd_dir, usb_dir):
        self.sd = sd_dir
        self.hd = hd_dir
        self.usb = usb_dir

    def copy_files_sd_to_hd(self) -> bool:
        """
        This method simply recursively copies all directories and files from source(PATH) to destination(PATH)
        and then verifies that the original files and new files are identical using verify_copy().

        :return: {bool} True if success, False if failure
        """

        try:
            for root, dirs, files in os.walk(self.sd):
                for file in files:

                    if os.path.exists(os.path.join(self.hd, file)):

                        filename, extension = file.split(sep='.')
                        filename += ' ' + secrets.token_hex(8) + '.' + extension

                        shutil.copy2(os.path.join(root, file), os.path.join(self.hd, filename))

                    else:
                        shutil.copy2(os.path.join(root, file), self.hd)

                    if filecmp.cmp(os.path.join(root, file), os.path.join(self.hd, file)):

                        print(f"Copied file '{file}' from SD card to SSD")

                    else:
                        print(f"Mismatched file '{file}'")
                        raise MismatchFileError

            return True

        except IOError or PermissionError or OSError as e:
            print(f"Copy Error: {e}")

            return False

    def upload_sd_data(self):
        pass

    def clear_sd_card(self):
        pass

    def download_flight_data(self):
        pass

    def clear_hd(self):
        pass

    def test(self):
        print(self.sd, self.hd)


if __name__ == '__main__':

    manager = DataManager()
    manager.copy_files_sd_to_hd()
