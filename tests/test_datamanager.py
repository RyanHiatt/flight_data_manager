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

    # clear sd
    data_manager.clear_sd_card()
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
    assert upload_from_sd_to_hd(10, True) == True


def test_dirty_upload_from_sd_to_hd():
    assert upload_from_sd_to_hd(10, False) == False


# test data download from hard drive to usb drive
def download_from_hd_to_usb_date(num_iter: int):

    data_manager.clear_hd()
    generate_simulated_hd(path=config.get('Paths', 'hd'), num_entries=100)

    iteration_results = []

    data_pool = data_manager.parse_hd_dates()['All']['dir_list']

    # loop x iterations
    for i in range(num_iter):
        iteration_results.append(data_manager.download_flight_data(data_pool))

    # get overall result
    if False in iteration_results:
        overall_result = False
    else:
        overall_result = True

    # return
    return overall_result


def test_download_from_hd_to_usb_date():
    assert download_from_hd_to_usb_date(10) == True


# test data download from hard drive to usb drive
def download_from_hd_to_usb_aircraft(num_iter: int):
    data_manager.clear_hd()
    generate_simulated_hd(path=config.get('Paths', 'hd'), num_entries=100)

    iteration_results = []

    data_pool = data_manager.parse_hd_aircraft()

    # loop x iterations
    for i in range(num_iter):
        iteration_results.append(data_manager.download_flight_data(data_pool))

    # get overall result
    if False in iteration_results:
        overall_result = False
    else:
        overall_result = True

    # return
    return overall_result


def test_download_from_hd_to_usb_aircraft():
    assert download_from_hd_to_usb_date(10) == True


# test data copy from sd card to usb drive
def copy_from_sd_to_usb(num_iter: int, clean_data: bool):

    # clear the sd card and start fresh
    data_manager.clear_sd_card()
    # simulate sd
    generate_simulated_sd(path=config.get('Paths', 'sd'), clean=clean_data)

    iteration_results = []

    # loop x iterations
    for i in range(num_iter):
        iteration_results.append(data_manager.copy_sd_to_usb())

    # get overall result
    if False in iteration_results:
        overall_result = False
    else:
        overall_result = True

    # return
    return overall_result


def test_copy_from_sd_to_usb():
    assert copy_from_sd_to_usb(10, True) == True


if __name__ == '__main__':
    pass
