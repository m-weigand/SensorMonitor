"""advetise available logger modules
"""
import datelogger
import tf_light

available_loggers = {}

available_loggers['datetime'] = datelogger.DateLogger
available_loggers['tf_light'] = tf_light.tf_light
available_loggers['tf_temp'] = tf_light.tf_temp
available_loggers['tf_moisture'] = tf_light.tf_moisture
