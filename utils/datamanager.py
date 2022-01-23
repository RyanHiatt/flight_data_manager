import os
import shutil
import configparser
import filecmp
import secrets


from utils.exceptions import MismatchFileError


class DataManager:

    config = configparser.ConfigParser()
    config.read('../config.cfg')

    @staticmethod
    def verify_copy(src: str, dst: str) -> bool:
        """
        This static method compares two files to determine if they are identical.

        :param src: {str} The path of the source
        :param dst: {str} The path of the destination
        :return: {bool}
        """
        return filecmp.cmp(src, dst)

    def copy_sd_data(self) -> bool:
        """
        This method simply recursively copies all directories and files from source(PATH) to destination(PATH)
        and then verifies that the original files and new files are identical using verify_copy().

        :return: {bool} True if success, False if failure
        """
        # TODO review path handling

        try:
            for root, dirs, files in os.walk(self.config['Paths']['sd_dir']):
                for file in files:

                    if os.path.exists(os.path.join(self.config['Paths']['hd_dir'], file)):

                        filename, extension = file.split(sep='.')
                        filename += ' ' + secrets.token_hex(8) + '.' + extension

                        shutil.copy2(os.path.join(root, file),
                                     os.path.join(self.config['Paths']['hd_dir'], filename))

                    else:
                        shutil.copy2(os.path.join(root, file),
                                     self.config['Paths']['hd_dir'])

                    if self.verify_copy(os.path.join(root, file),
                                        os.path.join(self.config['Paths']['hd_dir'], file)):

                        print(f"Copied file '{file}' from SD card to SSD")

                    else:
                        print(f"Mismatched file '{file}'")
                        raise MismatchFileError

            return True

        except IOError or PermissionError as e:
            print(f"Copy Error: {e}")

            return False

    def clear_sd_card(self):
        pass

    def download_flight_data(self):
        pass

    def clear_hd(self):
        pass

    def upload_flight_data(self):
        pass


if __name__ == '__main__':
    manager = DataManager()
    manager.copy_sd_data()
