#!/usr/bin/python
# *-* coding: utf-8 *-*
"""

"""
import datetime
import logging
import pandas as pd
import StringIO
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


def app_pages(app):

    def list_sensors():
        # generate a list of available loggers
        avail_sensors = []
        for key, item in sensors.available_loggers.iteritems():
            avail_sensors.append(
                (key, item.description())
            )

        # create a logger manager so we get a database connection
        logger_manager = get_logger_manager()
        db = logger_manager.db
        query = db['session'].query(db['sensors']).all()

        results = []
        for sensor in query:
            sensor_class = sensors.available_loggers[sensor.type]
            table = sensor_class.get_table(db['base'], db['engine'])

            query_last_entry = db['session'].query(table).filter_by(
                logger_id=sensor.id).order_by(
                table.id.desc()).first()

            query_first_entry = db['session'].query(table).filter_by(
                logger_id=sensor.id).order_by(
                table.id.asc()).first()

            total_nr = db['session'].query(table.id).filter_by(
                logger_id=sensor.id).count()

            print('COUNT: ', total_nr)
            results.append((sensor, query_first_entry,
                            query_last_entry, total_nr))

        return render_template(
            'sensor_manager.html',
            avail_sensors=avail_sensors,
            sensors=results
        )

    @app.route('/')
    def show_sensors():
        return list_sensors()

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

        return render_template(
            'show_sensor.html', sensor=query, plot_html=plot)

    @app.route('/add_sensor', methods=['POST', ])
    def add_sensor():
        logger_manager = LoggerManager(
            {'database_file': app.gsettings['database_file'],
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

    def get_logger_manager():
        """Create a logger manager for each request
        """
        logger_manager = getattr(g, '_logger_manager', None)
        if logger_manager is None:
            logger_manager = LoggerManager(
                {'database_file': app.gsettings['database_file'],
                 'interval': None})
            setattr(g, '_logger_manager', logger_manager)
        return logger_manager

    @app.route('/export_to_csv', methods=['GET', ])
    def export_sensor_to_csv():
        sensor_id = request.args.get('id', None, type=int)
        dt = request.args.get('dt', None)
        dt2 = request.args.get('datetime_1', None)
        print('DATETIME', dt, dt2)
        nr_data_points = request.args.get('nr_datapoints', None, type=int)

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

        query = db['session'].query(sensor_table).order_by(
            sensor_table.id.desc())
        if nr_data_points is not None:
            query = query.limit(nr_data_points)

        # create a DateFrame
        df = pd.read_sql_query(query.statement, db['engine'])
        df = df.set_index('id')
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
            {'database_file': app.gsettings['database_file'],
             'interval': None})
        db = logger_manager.db

        id_to_delete = request.args.get('id', '', type=int)
        query = db['session'].query(db['sensors']).filter_by(
            id=id_to_delete).first()

        query.status = state
        # db['session'].update(query).values(log=False)
        db['session'].add(query)
        db['session'].commit()

    return app


def create_app(cmdopts):
    app = Flask(__name__)
    app.debug = True

    global_settings = {}
    global_settings['database_file'] = cmdopts.database
    app.gsettings = global_settings
    app_pages(app)
    return app
