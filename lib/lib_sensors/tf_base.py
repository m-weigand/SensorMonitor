import baselogger
from tinkerforge.ip_connection import IPConnection
from bokeh.resources import CDN
# from bokeh.plotting import circle
# from bokeh.embed import autoload_static
from bokeh.embed import components
# import bokeh.plotting as bk
# from bokeh.charts import Line
from bokeh.plotting import figure
# from flask import url_for
import numpy as np


class tf_base(baselogger.BaseLogger):
    """Base class for all tinkerforge sensors
    """
    def __init__(self, db, threadID, name, logger_id, table, settings):
        baselogger.BaseLogger.__init__(self,
                                       db,
                                       threadID,
                                       name,
                                       logger_id,
                                       table,
                                       settings)

        self.name = name
        # settings is a string containing [HOST IP], [HOST PORT], [SENSOR UID],
        # separated by :
        tf_items = self.settings.split(':')
        if len(tf_items) != 3:
            raise IOError('Need three settings: IP, PORT, UID')

        self.host = tf_items[0]
        self.port = int(tf_items[1])
        self.uid = tf_items[2]

        self._connect_to_bricklet()

    def _connect_to_bricklet(self):
        # Create IP connection
        self.ipcon = IPConnection()

        self._create_device_obj()

        # Connect to brickd
        self.ipcon.connect(self.host, self.port)

    def _create_device_obj(self):
        print('Modify this place holder!')
        exit()

    def _disconnect(self):
        self.ipcon.disconnect()

    @staticmethod
    def plot(cls, db, logger_item):
        """For a given sensor instance, return a html snippet containing the
        plot (using bokeh).

        This is only a placeholder!

        Parameters
        ----------
        db: database object from sqlalchemy
        item: table row from the sensors database table describing this
              specific sensor.

        """
        table = cls.get_table(db['base'], db['engine'])
        query = db['session'].query(table).filter_by(
            logger_id=logger_item.id).all()

        # 2015-09-11 08:17:35.272359
        times = [x.datetime for x in query]
        values = [float(x.value) for x in query]

        indices = np.linspace(0, len(times), 1000)
        print('INDICES', indices)

        # create the bokeh plot
        p = figure(plot_width=800, plot_height=600, x_axis_type="datetime")
        p.line(times, values)
        # js, tag = autoload_static(
        #     p, CDN, url_for('static', filename="plot.js"))
        script, div = components(p, CDN)
        output_html = script + div

        # with open('static/plot.js', 'w') as fid:
        #     fid.write(js)

        # output_html = ''
        # output_html += tag
        return output_html
