#! /bin/sh
# start_app.sh
cd /
cd /home/pi/flight_data_manager/
git pull
python3 run.py
cd /