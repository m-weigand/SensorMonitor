import lib_sensors.sensors as sensors
# from flask import url_for
# import matplotlib as mpl
import pylab as plt
import cStringIO


def plot_temp(db, item):
    print 'plotting tf temp'
    tf_light = sensors.available_loggers['tf_temp']

    table = tf_light.get_table(db['base'], db['engine'])
    query = db['session'].query(table).all()
    times = [x.datetime for x in query]
    temperatures = [float(x.value) for x in query]

    x = range(0, len(temperatures))
    y = temperatures

    fig, ax = plt.subplots(1, 1)
    ax.set_title(item.name)
    ax.plot(times, y)
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

    fig, ax = plt.subplots(1, 1)
    ax.set_title(item.name)
    ax.plot(times, y)
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
