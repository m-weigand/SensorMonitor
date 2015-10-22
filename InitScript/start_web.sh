#!/bin/bash

/usr/local/bin/multi_sensor_manager_web.py  -d /home/mweigand/Projekte/SensorMonitor/Example2/sensors.db > /var/log/sensor_logger_logfile.log 2>&1 &
