"""advertise available logger modules
"""
import datelogger
import tf_light
import tf_temp
import tf_moisture

available_loggers = {}

available_loggers['datetime'] = datelogger.DateLogger
available_loggers['tf_light'] = tf_light.tf_light
available_loggers['tf_temp'] = tf_temp.sensor
available_loggers['tf_moisture'] = tf_moisture.tf_moisture
