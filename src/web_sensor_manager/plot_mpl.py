import lib_sensors.sensors as sensors
import numpy as np
# from flask import url_for
import matplotlib as mpl
mpl.use('Agg')
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


def plot_moisture(db, item):
    print 'plotting tf moisture'
    tf_light = sensors.available_loggers['tf_moisture']

    table = tf_light.get_table(db['base'], db['engine'])
    query = db['session'].query(table).all()
    times = [x.datetime for x in query]
    moisture = [float(x.value) for x in query]

    x = range(0, len(moisture))
    y = moisture / 1000.0
    x, y = reduce_xy(x, y, 100)

    fig, ax = plt.subplots(1, 1)
    ax.set_title(item.name)
    ax.plot(times, y, '.-')
    ax.set_ylabel('Moisture [mA]')
    format = "png"
    sio = cStringIO.StringIO()
    fig.autofmt_xdate()
    fig.savefig(sio, format=format)
    output_html = '<img src="data:image/png;base64,{0}"/>'.format(
        sio.getvalue().encode("base64").strip())
    return output_html


def plot_temp(db, item):
    print 'plotting tf temp'
    tf_light = sensors.available_loggers['tf_temp']

    table = tf_light.get_table(db['base'], db['engine'])
    query = db['session'].query(table).all()
    times = [x.datetime for x in query]
    temperatures = [float(x.value) for x in query]

    x = range(0, len(temperatures))
    y = temperatures
    x, y = reduce_xy(x, y, 100)

    fig, ax = plt.subplots(1, 1)
    ax.set_title(item.name)
    ax.plot(times, y, '.-')
    ax.set_ylabel('T [deg]')
    format = "png"
    sio = cStringIO.StringIO()
    fig.autofmt_xdate()
    fig.savefig(sio, format=format)
    output_html = '<img src="data:image/png;base64,{0}"/>'.format(
        sio.getvalue().encode("base64").strip())
    return output_html


def plot_light(db, item):
    print 'plotting tf light'
    tf_light = sensors.available_loggers['tf_light']

    table = tf_light.get_table(db['base'], db['engine'])
    query = db['session'].query(table).all()
    times = [x.datetime for x in query]
    illuminances = [float(x.value) for x in query]

    # filename_base = str(uuid.uuid4()) + '.png'
    # filename = 'static/' + filename_base

    """
    fig, ax = plt.subplots(1, 1)
    ax.set_title(item.name)
    ax.plot(times, illuminances, '.-')
    fig.autofmt_xdate()

    fig.savefig(filename)
    """

    x = range(0, len(illuminances))
    y = illuminances
    x, y = reduce_xy(x, y, 100)

    fig, ax = plt.subplots(1, 1)
    ax.set_title(item.name)
    ax.plot(times, y, '.-')
    format = "png"
    sio = cStringIO.StringIO()
    fig.savefig(sio, format=format)
    # print "Content-Type: image/%s\n" % format
    # msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    # # Needed this on windows, IIS
    # sys.stdout.write(sio.getvalue())

    output_html = '<img src="data:image/png;base64,{0}"/>'.format(
        sio.getvalue().encode("base64").strip())
    # output_html = '<img src="' + url_for('static', filename=filename_base)
    # output_html += '">'
    # output_html += tag
    return output_html
