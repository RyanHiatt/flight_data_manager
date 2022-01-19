import os
import shutil
import configparser
import filecmp


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
        # TODO append unique identifier
        # TODO review path handling
        # TODO handle directories

        try:
            for file in os.listdir(self.config['Paths']['sd_dir']):

                shutil.copy2(os.path.join(self.config['Paths']['sd_dir'], file),
                             self.config['Paths']['hd_dir'])

                if self.verify_copy(os.path.join(self.config['Paths']['sd_dir'], file),
                                    os.path.join(self.config['Paths']['hd_dir'], file)):

                    print(f"Copied file '{file}' from SD card to SSD")

                else:
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
