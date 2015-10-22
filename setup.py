#!/usr/bin/env python
from setuptools import setup
import os
import glob
# from setuptools import find_packages
# find_packages

# under windows, run
# python.exe setup.py bdist --format msi
# to create a windows installer

version_short = '0.1'
version_long = '0.1.0'

os.chdir('lib/lib_multi_sensor')
package_data = glob.glob('templates/*')
for x in os.walk('static'):
    for y in x[2]:
        package_data.append(x[0] + os.sep + y)
os.chdir('../../')

if __name__ == '__main__':
    setup(name='mx_sensor_logger',
          version=version_long,
          description='General sensor logger',
          author='Maximilian Weigand',
          author_email='mweigand@geo.uni-bonn.de',
          url='http://www.geo.uni-bonn.de/~mweigand',
          # find_packages() somehow does not work under Win7 when creating a
          # msi # installer
          # packages=find_packages(),
          include_package_data=True,
          package_data={'lib_multi_sensor': package_data},
          zip_safe=False,
          package_dir={'': 'lib'},
          packages=['lib_sensors',
                    'lib_sensors/web',
                    'lib_multi_sensor'],
          scripts=['src/sensor_logger/multi_sensor_logger.py',
                   'src/web_sensor_manager/multi_sensor_manager_web.py',
                   'InitScript/start_multi_sens_web.sh',
                   ],
          install_requires=['numpy', 'scipy', 'matplotlib']
          )
