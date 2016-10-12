"""advertise available logger modules
"""
import lib_sensors.datelogger
import lib_sensors.tf_barometer
import lib_sensors.tf_light
import lib_sensors.tf_temp
import lib_sensors.tf_moisture
import lib_sensors.w1_temp
import lib_sensors.ar_wt

available_loggers = {}

available_loggers['datetime'] = lib_sensors.datelogger.DateLogger
available_loggers['tf_barometer'] = lib_sensors.tf_barometer.tf_barometer
available_loggers['tf_light'] = lib_sensors.tf_light.tf_light
available_loggers['tf_temp'] = lib_sensors.tf_temp.sensor
available_loggers['tf_moisture'] = lib_sensors.tf_moisture.tf_moisture
available_loggers['w1_temp'] = lib_sensors.w1_temp.w1_temp
available_loggers['ar_wt'] = lib_sensors.ar_wt.arduino_wt
