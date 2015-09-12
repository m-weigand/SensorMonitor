#!/usr/bin/python
# *-* coding: utf-8 *-*
"""

"""
import logging
import os
# import sys
from optparse import OptionParser
# sys.path.append('../sensor_logger/')
from flask import Flask
from flask import render_template
from flask import request
# this is something like a per-request global object
from flask import g

from multi_sensor_logger import LoggerManager
import lib_sensors.sensors as sensors
# import lib_sensors.web.plot_bokeh as plot_funcs
# import lib_sensors.web.plot_mpl as plot_funcs
#

logging.basicConfig(filename='web.logfile.log',
                    level=logging.INFO)

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
        print('Need a valid database file! File not found:')
        print(options.database)
        exit()

    return options


@app.route('/')
def show_sensors():
    return render_sensors()


def render_sensors():
    # create a logger manager so we get a database connection
    logger_manager = get_logger_manager()
    db = logger_manager.db
    query = db['session'].query(db['sensors']).all()
    plots = []
    # add some counters for the divs
    nr_cols = 2
    col = 1
    for item in query:
        if col == 1:
            prefix = '<div class="row">'
        else:
            prefix = ''

        # get a sensor object of this type
        sensor_class = sensors.available_loggers[item.type]
        print 'item', item, dir(item), item.name, item.id
        plot = sensor_class.plot(sensor_class, db, item)
        # item.plot(db, item)
        # if item.type == 'tf_light':
        #     plot = plot_funcs.plot_light(db, item)
        # if item.type == 'tf_temp':
        #     plot = plot_funcs.plot_temp(db, item)
        # if item.type == 'tf_moisture':
        #     plot = plot_funcs.plot_moisture(db, item)

        plot = '<div style="width=600px; float:left;">' + plot + '</div><br />'

        if col == nr_cols:
            postfix = '</div><br />'
            col = 1
        else:
            postfix = ''
            col += 1

        plots.append(prefix + plot + postfix)
    # finish the div
    if col != 1:
        plots[-1] += '</div>'

    return render_template('sensor_manager.html', sensors=query, plots=plots)


@app.route('/show_sensor')
def show_sensor():
    return render_sensors()


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
    return render_sensors()


@app.route('/delete_sensor')
def delete_sensor():
    logger_manager = LoggerManager({})
    db = logger_manager.db

    id_to_delete = request.args.get('id', '', type=int)
    query = db['session'].query(db['sensors']).filter_by(
        id=id_to_delete).first()

    db['session'].delete(query)
    db['session'].commit()
    return render_sensors()


@app.route('/activate_sensor')
def activate_sensor():
    set_log(1)
    return render_sensors()


@app.route('/deactivate_sensor')
def deactivate_sensor():
    set_log(0)
    return render_sensors()


def set_log(state):
    logger_manager = LoggerManager({})
    db = logger_manager.db

    id_to_delete = request.args.get('id', '', type=int)
    query = db['session'].query(db['sensors']).filter_by(
        id=id_to_delete).first()

    query.status = state
    # db['session'].update(query).values(log=False)
    db['session'].add(query)
    db['session'].commit()
    return render_sensors()


def prepare_directory():
    if not os.path.isdir('static'):
        os.makedirs('static')

if __name__ == '__main__':
    logging.info('Multi sensor logger started')
    prepare_directory()
    options = handle_cmd_options()
    global_settings['database_file'] = options.database
    app.run('0.0.0.0')
