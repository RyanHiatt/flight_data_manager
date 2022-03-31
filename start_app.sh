#! /bin/sh
# start_app.sh
cd /
cd /home/pi/flight_data_manager/
git pull
sleep 5
python3 run.py
cd /