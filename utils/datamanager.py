import os
import shutil
import configparser
import filecmp
import secrets
import logging
from xml.etree import ElementTree
from datetime import datetime

from utils.exceptions import MismatchFileError


# Instantiate configparser and read config
config = configparser.ConfigParser()
config.read('config.ini')


# Instantiate logging
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.DEBUG)

# Create file handler and set level
file_handler = logging.FileHandler(filename=config.get("Paths", "base_path") + "/logs/data_manager.log",
                                   mode='w', encoding='utf-8')
file_handler.setLevel(level=logging.DEBUG)

# Create formatter
formatter = logging.Formatter(fmt="[%(levelname)s]\t%(asctime)s:\t%(message)s", datefmt='%Y-%m-%d %H:%M:%S')

# Add formatter to file handler
file_handler.setFormatter(fmt=formatter)

# Add file handler to logger
logger.addHandler(hdlr=file_handler)


class DataManager:

    # File parsing variables
    target = config.get('Xml Parsing', 'file_target')
    name_conv_par1 = config.get('Xml Parsing', 'param_1')
    name_conv_par2 = config.get('Xml Parsing', 'param_2')

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
            logger.error(f"Existing Directory Error: {e}")

    @staticmethod
    def verify_dir_copy(src: str, dst: str) -> bool:
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

    @staticmethod
    def verify_file_copy(src: str, dst: str) -> bool:
        """
        This method compares two files and determines if there are any differences
        :param src: {str} The source file being compared against
        :param dst: {dst} The destination file beging compared
        :return: {bool} True if the files match, False if they do not match
        """
        # Instantiate a dircmp object and extract differing files
        dir_comp = filecmp.cmp(src, dst)

        if dir_comp:  # if the same
            return True
        else:  # if different
            return False

    def _parse_airframe_info_xml(self, xml_file_path: str) -> tuple:
        """
        This method takes a xml file to parse and finds the two parameters specified in the config.ini
        :param xml_file_path: {str} The path to the desired xml file
        :return: {tuple} Returns (parameter 1 value, parameter 2 value)
        """
        # Get the xml tree structure
        tree = ElementTree.parse(xml_file_path)
        # extract the root element of the tree
        root = tree.getroot()
        # Find the defined children of the root
        param1 = root.find(f"./{self.name_conv_par1}").text
        param2 = root.find(f"./{self.name_conv_par2}").text

        return param1, param2

    @staticmethod
    def _find_target(path: str, file: str) -> bool:
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
                    return True
                else:
                    return False

        except IOError or PermissionError or OSError as e:
            logger.error(f"SD Card Error: {e}")

    @staticmethod
    def _select_files(path: str):
        """

        :param path:
        :return:
        """
        target_dirs = config.get('File Selection', 'directories').split(sep=',')
        target_files = config.get('File Selection', 'files').split(sep=',')

        dir_selection = []
        file_selection = []

        try:
            # Walk through all the files on the sd card
            for root, dirs, files in os.walk(path):
                for directory in dirs:
                    for target_dir in target_dirs:
                        if target_dir in directory:
                            dir_selection.append(os.path.join(root, directory))
                for file in files:
                    for target_file in target_files:
                        if target_file in file:
                            file_selection.append(os.path.join(root, file))

            return dir_selection, file_selection

        except IOError or PermissionError or OSError as e:
            logger.error(f"SD Card Error: {e}")

    def upload_flight_data(self):
        """


        :return:
        """
        # Check if the target exists -> return bool and path
        result = self._find_target(path=config.get('Paths', 'sd'), file=self.target)

        if result:  # Continue with target file
            target_path = os.path.join(config.get('Paths', 'sd'), self.target)

            # parse the target file to find naming parameters
            param1, param2 = self._parse_airframe_info_xml(xml_file_path=target_path)

            # Generate the directory name based on the two xml parameters
            dst_dir_name = param1 + '-' + param2

            # Generate directory with ISO 8601 stamp
            new_entry = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

            # Select files for copy
            directories, files = self._select_files(path=config.get('Paths', 'sd'))

            # Copy relevant directories to hard drive
            for directory in directories:
                shutil.copytree(directory, dst=os.path.join(config.get('Paths', 'hd'), dst_dir_name, new_entry))
                if self.verify_dir_copy(src=directory,
                                        dst=os.path.join(config.get('Paths', 'hd'), dst_dir_name, new_entry)):
                    logger.info(f"Successful copied {directory.split(sep='/')[-1]} to {dst_dir_name}/{new_entry}")
                else:
                    logger.warning(f"Mismatched dir {directory.split(sep='/')[-1]} and {dst_dir_name}/{new_entry}")

            # Copy relevant files to hard drive
            for file in files:
                shutil.copy2(file, dst=os.path.join(config.get('Paths', 'hd'), dst_dir_name, new_entry))
                if self.verify_file_copy(src=file,
                                         dst=os.path.join(config.get('Paths', 'hd'), dst_dir_name, new_entry, file)):
                    logger.info(f"Successful copied {file.split(sep='/')[-1]} to {dst_dir_name}/{new_entry}")
                else:
                    logger.warning(f"Mismatched file {file.split(sep='/')[-1]} and {dst_dir_name}/{new_entry}")

            return True

        else:  # Target does not exist
            return False

    def copy_sd_to_usb(self):
        try:
            shutil.copytree(src=config.get('Paths', 'sd'),
                            dst=f"{config.get('Paths', 'usb')}/FlightData")
            if self.verify_dir_copy(src=config.get('Paths', 'sd'),
                                    dst=f"{config.get('Paths', 'usb')}/FlightData"):
                logger.info(f"Successful copied {config.get('Paths', 'sd')} to "
                            f"{os.path.join(config.get('Paths', 'usb'), 'FlightData')}")
            else:
                logger.warning(f"Mismatched file {config.get('Paths', 'sd')} and "
                               f"{os.path.join(config.get('Paths', 'usb'), 'FlightData')}")

        except Exception as e:
            logger.warning(f"SD to USB transfer error: {e}")

    @staticmethod
    def clear_sd_card():

        for filename in os.listdir(config.get('Paths', 'sd')):
            file_path = os.path.join(config.get('Paths', 'sd'), filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to clear sd card {file_path}. Reason: {e}")

    def download_flight_data(self):
        pass

    @staticmethod
    def clear_hd():

        for filename in os.listdir(config.get('Paths', 'hd')):
            file_path = os.path.join(config.get('Paths', 'hd'), filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to clear sd card {file_path}. Reason: {e}")

    @staticmethod
    def copy_files(src, dst) -> bool:
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

                        logger.info(f"Copied file '{file}'")

                    else:
                        logger.warning(f"Mismatched file '{file}'")
                        raise MismatchFileError

            return True

        except IOError or PermissionError or OSError as e:
            logger.error(f"Copy Error: {e}")

            return False


if __name__ == '__main__':

    manager = DataManager()
    manager.upload_flight_data()
