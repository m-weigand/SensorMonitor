#!/bin/bash

test -d dist && rm -r dist
python setup.py sdist
cd dist
mv mx_sensor_logger-0.1.0.tar.gz mx-sensor-logger_0.1.0.orig.tar.gz
tar xvzf mx-sensor-logger_0.1.0.orig.tar.gz
cd mx_sensor_logger-0.1.0
cp -r ../../debian .
dpkg-buildpackage -uc -us

