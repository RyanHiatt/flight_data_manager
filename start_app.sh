#! /bin/sh
# start_app.sh
cd /
cd /home/pi/flight_data_manager/
git reset --hard origin/master
sleep 3
python3 run.py
cd /
