#!/usr/bin/python
"""
Create a new database and add test sensors
"""
import sensor_logger as SL

settings = {'interval': 5}
LoggerManager = SL.LoggerManager(settings)
db = LoggerManager.db

"""
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
"""

# sensor 3 tf_light
ins = db['sensors'](type='tf_light', name='light 1',
                    interval=5, log=True, settings='pi:4223:asU')
                    # interval=5, log=True, settings='127.0.0.1:4223:asU')
db['session'].add(ins)
db['session'].commit()

ins = db['sensors'](type='tf_temp', name='temp 1',
                    interval=3, log=True, settings='pi:4223:6JW')
                    # interval=3, log=True, settings='127.0.0.1:4223:6JW')
db['session'].add(ins)
db['session'].commit()

ins = db['sensors'](type='tf_temp', name='temp 2',
                    # interval=3, log=True, settings='pi:4223:npD')
                    interval=3, log=True, settings='127.0.0.1:4223:npD')
db['session'].add(ins)
db['session'].commit()

"""
ins = db['sensors'](type='tf_moisture', name='moisture 1',
                    interval=3, log=True, settings='127.0.0.1:4223:kwY')
db['session'].add(ins)
db['session'].commit()
"""
