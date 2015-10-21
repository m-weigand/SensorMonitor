#!/usr/bin/python
# *-* coding: utf-8 *-*
"""

"""
import datetime
import logging
import os
import pandas as pd
import StringIO
# import sys
from optparse import OptionParser
# sys.path.append('../sensor_logger/')
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
# this is something like a per-request global object
from flask import g
from flask import redirect
from flask import url_for

from multi_sensor_logger import LoggerManager
import lib_sensors.sensors as sensors
# import lib_sensors.web.plot_bokeh as plot_funcs
# import lib_sensors.web.plot_mpl as plot_funcs
#

logging.basicConfig(level=logging.INFO,
                    # filename='web.logfile.log',
                    )

app = Flask(__name__)
app.debug = True

global_settings = {}


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


@app.route('/')
def show_sensors():
    return list_sensors()


def list_sensors():
    # create a logger manager so we get a database connection
    logger_manager = get_logger_manager()
    db = logger_manager.db
    query = db['session'].query(db['sensors']).all()

    return render_template('sensor_manager.html', sensors=query)


@app.route('/show_sensor', methods=['GET', ])
def show_sensor():
    logger_id = request.args.get('id', None)
    if logger_id is None:
        return redirect(url_for('show_sensors'))

    logger_manager = get_logger_manager()
    db = logger_manager.db
    query = db['session'].query(db['sensors']).filter_by(
        id=logger_id).first()
    sensor_class = sensors.available_loggers[query.type]
    plot = sensor_class.plot(sensor_class, db, query)

    return render_template('show_sensor.html', sensor=query, plot_html=plot)


def get_logger_manager():
    """Create a logger manager for each request
    """
    logger_manager = getattr(g, '_logger_manager', None)
    if logger_manager is None:
        logger_manager = LoggerManager(
            {'database_file': global_settings['database_file'],
             'interval': None})
        setattr(g, '_logger_manager', logger_manager)
    return logger_manager


@app.route('/add_sensor', methods=['POST', ])
def add_sensor():
    logger_manager = LoggerManager(
        {'database_file': global_settings['database_file'],
         'interval': None})
    db = logger_manager.db
    name = request.form['name']
    sensor_type = request.form['type']
    interval = request.form['interval']
    settings = request.form['settings']
    ins = db['sensors'](type=sensor_type, name=name,
                        interval=interval, status=1,
                        settings=settings)
    db['session'].add(ins)
    db['session'].commit()
    return redirect(url_for('show_sensors'))


@app.route('/delete_sensor')
def delete_sensor():
    logger_manager = LoggerManager({})
    db = logger_manager.db

    id_to_delete = request.args.get('id', '', type=int)
    query = db['session'].query(db['sensors']).filter_by(
        id=id_to_delete).one()

    db['session'].delete(query)
    db['session'].commit()
    return redirect(url_for('show_sensors'))


@app.route('/export_to_csv', methods=['GET', ])
def export_sensor_to_csv():
    sensor_id = request.args.get('id', None, type=int)
    if sensor_id is None:
        # TODO: Show error message
        return redirect(url_for('show_sensors'))

    # create a logger manager so we get a database connection
    logger_manager = get_logger_manager()
    db = logger_manager.db
    query = db['session'].query(db['sensors']).filter_by(
        id=sensor_id).one()
    sensor_class = sensors.available_loggers[query.type]
    sensor_table = sensor_class.get_table(db['base'], db['engine'])
    query = db['session'].query(sensor_table)

    # create a DateFrame
    df = pd.read_sql(query.statement, db['engine']).set_index('id')
    # save to CSV file in memory
    csv_in_memory = StringIO.StringIO()
    df.to_csv(csv_in_memory)
    csv_in_memory.seek(0)  # rewind

    filename = '{0}_data_{1}.csv'.format(
        datetime.datetime.now(),
        sensor_table.__tablename__)

    return send_file(csv_in_memory,
                     as_attachment=True,
                     attachment_filename=filename)


@app.route('/activate_sensor')
def activate_sensor():
    set_log(1)
    return redirect(url_for('show_sensors'))


@app.route('/deactivate_sensor')
def deactivate_sensor():
    set_log(0)
    return redirect(url_for('show_sensors'))


def set_log(state):
    logger_manager = LoggerManager(
        {'database_file': global_settings['database_file'],
         'interval': None})
    db = logger_manager.db

    id_to_delete = request.args.get('id', '', type=int)
    query = db['session'].query(db['sensors']).filter_by(
        id=id_to_delete).first()

    query.status = state
    # db['session'].update(query).values(log=False)
    db['session'].add(query)
    db['session'].commit()


def prepare_directory():
    if not os.path.isdir('static'):
        os.makedirs('static')

if __name__ == '__main__':
    logging.info('Multi sensor logger started')
    prepare_directory()
    options = handle_cmd_options()
    global_settings['database_file'] = options.database
    app.run('0.0.0.0')
