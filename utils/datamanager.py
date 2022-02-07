import os
import shutil
import configparser
import filecmp
import secrets
from xml.etree import ElementTree as ET
from datetime import datetime


from utils.exceptions import MismatchFileError


class DataManager:

    # Instantiate configparser and read config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Drive Paths
    sd_path = config.get('Paths', 'sd')
    hd_path = config.get('Paths', 'hd')
    usb_path = config.get('Paths', 'usb')

    # File parsing variables
    target = config.get('File Parsing', 'sd_target')
    name_conv_par1 = config.get('File Parsing', 'param_1')
    name_conv_par2 = config.get('File Parsing', 'param_2')

    @staticmethod
    def dir_exists(dst: str, reference: str) -> bool:
        """
        Given a top level directory, this method simply looks if a specific reference directory
        exists within the tree.
        :param dst: {str} A top level directory to search through
        :param reference: {str} The reference directory being searched for
        :return: {bool} True if the reference dir exists, False if it does not exist
        """
        try:
            # Walk through all directories
            for root, dirs, files in os.walk(dst):
                # Check if reference dir is in the dirs list
                if reference in dirs:
                    return True
                else:
                    return False

        except IOError or PermissionError or OSError as e:
            print(f"Existing Directory Error: {e}")

    @staticmethod
    def verify_copy(src: str, dst: str) -> bool:
        """
        This method compares two directories and determines if there are any differences
        :param src: {str} The source directory being compared against
        :param dst: {dst} The destination directory beging compared
        :return: {bool} True if the directories match, False if they do not match
        """
        # Instantiate a dircmp object and extract differing files
        dir_comp = filecmp.dircmp(src, dst).diff_files

        if dir_comp:  # if differing files, return false
            return False
        else:  # if no differing files, return true
            return True

    def _parse_airframe_info_xml(self, xml_file: str) -> tuple:
        """
        This method takes a xml file to parse and finds the two parameters specified in the config.ini
        :param xml_file: {str} The path to the desired xml file
        :return: {tuple} Returns (parameter 1 value, parameter 2 value)
        """
        # Get the xml tree structure
        tree = ET.parse(xml_file)
        # extract the root element of the tree
        root = tree.getroot()
        # Find the defined children of the root
        param1 = root.find(f"./{self.name_conv_par1}").text
        param2 = root.find(f"./{self.name_conv_par2}").text

        return param1, param2

    @staticmethod
    def _get_file_path(path: str, file: str) -> tuple:
        """
        This method gets the absolute path for a given file in a given directory
        :param path: {str} The path at which to begin the search
        :param file: {str} The file being searched for
        :return:
        """
        try:
            # Walk through all the files on the sd card
            for root, dirs, files in os.walk(path):
                # If one of the files is equal to the param file
                if file in files:
                    # Return the full path of the found file
                    return True, os.path.join(root, file)
                else:
                    return False, root

        except IOError or PermissionError or OSError as e:
            print(f"SD Card Error: {e}")

    def upload_sd_data_to_hd(self):
        """


        :return:
        """
        # Check if the target exists -> return bool and path
        result, target_path = self._get_file_path(path=self.sd_path, file=self.target)

        if result:  # Continue with target file

            # parse the target file to find naming parameters
            param1, param2 = self._parse_airframe_info_xml(xml_file=target_path)

            # Generate the directory name based on the two xml parameters
            dst_dir_name = param1 + '-' + param2

            # Generate directory with ISO 8601 stamp
            new_dir_name = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

            # Copy sd file structure to new directory
            shutil.copytree(src=self.sd_path, dst=os.path.join(self.hd_path, dst_dir_name, new_dir_name))

            # Verify that the copied files match the original
            if self.verify_copy(src=self.sd_path, dst=os.path.join(self.hd_path, dst_dir_name, new_dir_name)):
                print(f'Successful Copied: {dst_dir_name}/{new_dir_name}')
                return True
            else:
                print(f'Mismatched File: {dst_dir_name}/{new_dir_name}')
                raise MismatchFileError

        else:  # Target does not exist,
            return False

    def clear_sd_card(self):
        pass

    def download_flight_data(self):
        pass

    def clear_hd(self):
        pass

    def test(self):
        print(self.sd_path, self.hd_path)

    @staticmethod
    def copy_files(self, src, dst) -> bool:
        """
        This method simply recursively copies all files from source(PATH) to destination(PATH)
        and then verifies that the original files and new files are identical using verify_copy().

        :return: {bool} True if success, False if failure
        """
        try:
            for root, dirs, files in os.walk(src):
                for file in files:

                    if os.path.exists(os.path.join(dst, file)):

                        filename, extension = file.split(sep='.')
                        filename += ' ' + secrets.token_hex(8) + '.' + extension

                        shutil.copy2(os.path.join(root, file), os.path.join(dst, filename))

                    else:
                        shutil.copy2(os.path.join(root, file), dst)

                    if filecmp.cmp(os.path.join(root, file), os.path.join(dst, file)):

                        print(f"Copied file '{file}'")

                    else:
                        print(f"Mismatched file '{file}'")
                        raise MismatchFileError

            return True

        except IOError or PermissionError or OSError as e:
            print(f"Copy Error: {e}")

            return False


if __name__ == '__main__':

    manager = DataManager()
    manager.upload_sd_data_to_hd()
