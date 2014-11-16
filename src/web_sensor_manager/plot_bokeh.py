import lib_sensors.sensors as sensors
from flask import url_for


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

    # try bokeh
    from bokeh.resources import CDN
    # from bokeh.plotting import circle
    from bokeh.embed import autoload_static
    import bokeh.plotting as bk

    # plot = circle([1, 2], [3, 4])
    plot = bk.line(range(0, len(illuminances)), illuminances, line_width=2)

    x = range(0, len(illuminances))
    y = illuminances
    # print 'x', x
    print len(x), len(y)
    # xs = [0, 1, 2, 3, 4, 5]
    # ys = [x**2 for x in xs]
    plot = bk.line(times, y, line_width=2, x_axis_type="datetime")

    js, tag = autoload_static(plot, CDN, url_for('static', filename="plot.js"))

    with open('static/plot.js', 'w') as fid:
        fid.write(js)

    output_html = ''
    # output_html = '<img src="' + url_for('static', filename=filename_base)
    # output_html += '">'
    output_html += tag
    return output_html
