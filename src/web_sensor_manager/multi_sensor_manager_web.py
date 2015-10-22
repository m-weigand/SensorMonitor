#!/usr/bin/python
# *-* coding: utf-8 *-*
"""

"""
import logging
import os
from optparse import OptionParser
import lib_multi_sensor.app

logging.basicConfig(level=logging.INFO,
                    # filename='web.logfile.log',
                    )


def handle_cmd_options():
    parser = OptionParser()
    parser.add_option("-d", "--database", dest="database",
                      type='string', help="Database file",
                      metavar="FILE", default=None)

    (options, args) = parser.parse_args()

    if options.database is None or not os.path.isfile(options.database):
        logging.error('Need a valid database file! File not found:')
        logging.error(options.database)
        exit()

    return options


def prepare_directory():
    if not os.path.isdir('static'):
        os.makedirs('static')

if __name__ == '__main__':
    logging.info('Multi sensor logger started')
    prepare_directory()
    options = handle_cmd_options()
    app = lib_multi_sensor.app.create_app(cmdopts=options)

    # run application
    app.run('0.0.0.0')
