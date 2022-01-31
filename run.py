from app.flightdata import FlightDataApp
import filecmp
import os
import sys

base_path = os.path.dirname(os.path.abspath(__file__))
print(f'App started in {base_path}')
sys.path.insert(0, base_path)

if __name__ == '__main__':
    filecmp.clear_cache()
    FlightDataApp().run()
