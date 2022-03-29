import configparser

from tests.simulation_functions import generate_simulated_hd, generate_simulated_sd
from utils.datamanager import DataManager
from utils.devicemanager import DeviceManager


# Instantiate configparser and read config
config = configparser.ConfigParser()
config.read('config.ini')

# Instantiate DeviceManager
device_manager = DeviceManager()
device_manager.check_for_devices()

# Instantiate DataManager
data_manager = DataManager()


# test data upload from sd card to hard drive
def upload_from_sd_to_hd(num_iter: int, clean_data: bool) -> bool:

    overall_result = None
    iteration_results = []

    # loop x iterations
    for i in range(num_iter):

        # simulate sd
        generate_simulated_sd(path=config.get('Paths', 'sd'), clean=clean_data)

        # perform upload
        iteration_results.append(data_manager.upload_flight_data())

        # clear sd
        data_manager.clear_sd_card()

    # get overall result
    if False in iteration_results:
        overall_result = False
    else:
        overall_result = True

    # return
    return overall_result


def test_clean_upload_from_sd_to_hd():
    assert upload_from_sd_to_hd(100, True) == True


def test_dirty_upload_from_sd_to_hd():
    assert upload_from_sd_to_hd(100, False) == True


# test parse_hd_dates
def dl_parse_hd_dates():
    pass


# test parse_hd_aircraft
def dl_parse_hd_aircraft():
    pass


# test data download from hard drive to usb drive
def download_from_hd_to_usb():
    pass


def test_download_from_hd_to_usb():
    pass


# test data copy from sd card to usb drive
def test_copy_from_sd_to_usb():
    pass





if __name__ == '__main__':
    pass
