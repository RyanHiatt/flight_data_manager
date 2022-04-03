#! /bin/sh
# start_app.sh
cd /
cd /home/pi/flight_data_manager/
git pull
sleep 3
python3 run.py
cd /