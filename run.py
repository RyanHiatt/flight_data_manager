import filecmp
import os
import sys
import configparser

from app.flightdata import FlightDataApp

# TESTING TESTING
from utils.datamanager import DataManager

# manager = DataManager()
# manager.upload_sd_data_to_hd()
# ---------------

def setup():
    # Clear file comparison cache
    filecmp.clear_cache()

    # Initialize and read the config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Find the base_path of the app
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Update the config with the base path of the app
    config.set('Paths', 'base_path', base_path)

    # Insert base_path into system memory for efficient importing
    sys.path.insert(0, base_path)

    print(f'App started in {base_path}')


if __name__ == '__main__':
    setup()
    FlightDataApp().run()
