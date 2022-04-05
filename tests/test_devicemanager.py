import configparser

from utils.devicemanager import DeviceManager
from utils.datamanager import DataManager


# Instantiate configparser and read config
config = configparser.ConfigParser()
config.read('config.ini')

# Instantiate DeviceManager
device_manager = DeviceManager()
device_manager.check_for_devices()

# Instantiate DataManager
data_manager = DataManager()


# test capacity check
def capacity_check(num_iter: int):

    iteration_results = []

    # loop x iterations
    for i in range(num_iter):
        if device_manager.check_device_capacity(config.get('Paths', 'hd'), 'HD'):
            iteration_results.append(True)

    # get overall result
    if False in iteration_results:
        overall_result = False
    else:
        overall_result = True

    # return
    return overall_result


def test_capacity_check():
    assert capacity_check(100) == True


# test sd card detection and handling
def detect_and_handle_sd(num_iter: int):

    iteration_results = []

    # loop x iterations
    for i in range(num_iter):
        iteration_results.append(device_manager.check_for_sd())

    # get overall result
    if False in iteration_results:
        overall_result = False
    else:
        overall_result = True

    # return
    return overall_result


def test_detect_and_handle_sd():
    assert detect_and_handle_sd(100) == True


# test usb drive detection and handling
def detect_and_handle_usb(num_iter: int):

    iteration_results = []

    # loop x iterations
    for i in range(num_iter):
        iteration_results.append(device_manager.check_for_usb())

    # get overall result
    if False in iteration_results:
        overall_result = False
    else:
        overall_result = True

    # return
    return overall_result


def test_detect_and_handle_usb():
    assert detect_and_handle_usb(100) == True


# test hd detection and handling
def detect_and_handle_hd(num_iter: int):

    iteration_results = []

    # loop x iterations
    for i in range(num_iter):
        iteration_results.append(device_manager.locate_hd())

    # get overall result
    if False in iteration_results:
        overall_result = False
    else:
        overall_result = True

    # return
    return overall_result


def test_detect_and_handle_hd():
    assert detect_and_handle_hd(100) == True


if __name__ == '__main__':
    pass
