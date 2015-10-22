#!/bin/bash

odir="/multi_sensor"
test -d "${odir}" || mkdir "${odir}"

/usr/local/bin/multi_sensor_manager_web.py  -d "${odir}"/sensors.db > "${odir}"/sensor_logger_logfile.log 2>&1 &
