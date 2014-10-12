#!/usr/bin/python
"""
Create a new database and add test sensors
"""
import sensor_logger as SL

settings = {'interval': 5}
LoggerManager = SL.LoggerManager(settings)
db = LoggerManager.db

# ########## DateLogger ############
# sensor 1
ins = db['sensors'](type='datetime', name='date1',
                    interval=5,
                    log=True)

db['session'].add(ins)
db['session'].commit()

# sensor 2
ins = db['sensors'](type='datetime', name='date2',
                    interval=10, log=True)
db['session'].add(ins)
db['session'].commit()

# sensor 3 tf_light
ins = db['sensors'](type='tf_light', name='light 1',
                    interval=5, log=True)
db['session'].add(ins)
db['session'].commit()
