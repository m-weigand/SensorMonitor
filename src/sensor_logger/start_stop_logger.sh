#!/bin/bash
if [ ! $# -eq 1 ]; then
    echo "We require one argument: start|stop"
    exit
fi

action="$1"

if [ $action == "start" ]; then
    echo "start"
    multi_sensor_logger.py > logfile.log 2>&1 &
    pid=$!
    echo $pid > pid.run
elif [ $action == "stop" ]; then
    echo "stop"
    cat pid.run
    kill -15 `cat pid.run`
    # pgrep sensor_logger.py -i 15
fi
