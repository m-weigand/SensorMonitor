import lib_sensors.sensors as sensors
import numpy as np
# from flask import url_for
import matplotlib as mpl
mpl.use('Agg')
mpl.rcParams['font.size'] = 8.0
import pylab as plt
import cStringIO


def reduce_xy(x, y, number):
    """return reduced versions of x and y with number entries
    """
    total_nr = len(x)
    steplength = np.ceil(total_nr / float(number)).astype(int)
    indices = range(0, total_nr, steplength)
    xl = []
    yl = []
    for index in indices:
        xl.append(x[index])
        yl.append(y[index])
    return np.array(xl), np.array(yl)


def _plot_ts_to_html(data):
    """Plot a time series and return the plot embedded as base64 into html
    data = {'time': array containing timestamps,
            'y': y data array,
            'ylabel': label for y axis,
            'title': title string
            }
    """
    fig, ax = plt.subplots(1, 1, figsize=(4.8, 3.5), dpi=300)
    fig.subplots_adjust(top=0.90, bottom=0.2)
    ax.set_title(data['title'])
    ax.plot(data['times'], data['y'], '.-')
    ax.set_ylabel(data['ylabel'])
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter(r'%d.%m - %H:%M'))
    fig.autofmt_xdate()
    format = "png"
    sio = cStringIO.StringIO()
    fig.savefig(sio, format=format)
    fig.clf()
    plt.close(fig)

    output_html = '<img width="600px" src="data:image/png;base64,{0}"/>'.format(
        sio.getvalue().encode("base64").strip())
    return output_html


def plot_light(db, item):
    print 'plotting tf light'
    tf_light = sensors.available_loggers['tf_light']

    table = tf_light.get_table(db['base'], db['engine'])
    query = db['session'].query(table).filter_by(name=item.name).all()
    times = [x.datetime for x in query]
    illuminances = [float(x.value) for x in query]
    y = illuminances
    times, y = reduce_xy(times, y, 100)

    output_html = _plot_ts_to_html({'times': times,
                                    'y': y,
                                    'ylabel': '[Lux]',
                                    'title': item.name
                                    })
    return output_html


def plot_moisture(db, item):
    print 'plotting tf moisture'
    tf_light = sensors.available_loggers['tf_moisture']

    table = tf_light.get_table(db['base'], db['engine'])
    query = db['session'].query(table).filter_by(name=item.name).all()
    times = [x.datetime for x in query]
    moisture = np.array([float(x.value) for x in query])

    # x = range(0, len(moisture))
    y = moisture / 1000.0
    times, y = reduce_xy(times, y, 100)

    output_html = _plot_ts_to_html({'times': times,
                                    'y': y,
                                    'ylabel': 'Moisture [mA?]',
                                    'title': item.name
                                    })
    return output_html


def plot_temp(db, item):
    print 'plotting tf temp'
    tf_light = sensors.available_loggers['tf_temp']

    table = tf_light.get_table(db['base'], db['engine'])
    query = db['session'].query(table).filter_by(name=item.name).all()
    if len(query) == 0:
        return '<div>No data entries for sensors {0} of type {1}'.format(
            item.name, 'tf_temp')
    times = [x.datetime for x in query]
    temperatures = [float(x.value) for x in query]

    # x = range(0, len(temperatures))
    y = temperatures
    times, y = reduce_xy(times, y, 100)

    output_html = _plot_ts_to_html({'times': times,
                                    'y': y,
                                    'ylabel': 'Temp [deg]',
                                    'title': item.name
                                    })
    return output_html
