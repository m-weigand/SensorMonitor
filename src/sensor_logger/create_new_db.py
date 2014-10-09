#!/usr/bin/python
"""
Create a new database and add test sensors
"""
import sensor_logger as SL

db = SL.create_database()

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
