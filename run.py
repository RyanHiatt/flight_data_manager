import os
import sys
import configparser


def setup():

    # Initialize and read the config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Find the base_path of the app
    base_path = os.getcwd()

    # Update the config with the base path of the app
    config.set('Paths', 'base_path', base_path)

    # Save base_path to config file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    # Insert base_path into system memory for efficient importing
    sys.path.insert(0, base_path)

    print(f'App started in {base_path}')


if __name__ == '__main__':
    setup()

    from app.flightdata import FlightDataApp
    FlightDataApp().run()
