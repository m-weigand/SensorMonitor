#!/usr/bin/python
import sys
sys.path.append('../sensor_logger/')
from flask import Flask
from flask import render_template
# from flask import url_for
from sensor_logger import LoggerManager
# import lib_sensors.sensors as sensors
from flask import request

# import plot_bokeh as plot_funcs
import plot_mpl as plot_funcs

app = Flask(__name__)
app.debug = True


@app.route('/')
def show_sensors():
    return render_sensors()


def render_sensors():
    logger_manager = LoggerManager({})
    db = logger_manager.db
    query = db['session'].query(db['sensors']).all()
    plots = []
    for item in query:
        if item.type == 'tf_light':
            plot = plot_funcs.plot_light(db, item)
            plots.append(plot)
        if item.type == 'tf_temp':
            plot = plot_funcs.plot_temp(db, item)
            plots.append(plot)
        if item.type == 'tf_moisture':
            plot = plot_funcs.plot_moisture(db, item)
            plots.append(plot)

    return render_template('sensor_manager.html', sensors=query, plots=plots)


@app.route('/show_sensor')
def show_sensor():
    return render_sensors()


@app.route('/add_sensor', methods=['POST', ])
def add_sensor():
    logger_manager = LoggerManager({})
    db = logger_manager.db
    name = request.form['name']
    sensor_type = request.form['type']
    interval = request.form['interval']
    settings = request.form['settings']
    ins = db['sensors'](type=sensor_type, name=name,
                        interval=interval, log=True,
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
    set_log(True)
    return render_sensors()


@app.route('/deactivate_sensor')
def deactivate_sensor():
    set_log(False)
    return render_sensors()


def set_log(state):
    logger_manager = LoggerManager({})
    db = logger_manager.db

    id_to_delete = request.args.get('id', '', type=int)
    query = db['session'].query(db['sensors']).filter_by(
        id=id_to_delete).first()

    query.log = state
    # db['session'].update(query).values(log=False)
    db['session'].add(query)
    db['session'].commit()
    return render_sensors()

if __name__ == '__main__':
    app.run('0.0.0.0')
