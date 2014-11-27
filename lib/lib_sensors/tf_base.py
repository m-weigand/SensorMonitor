import datetime
import baselogger
from tinkerforge.ip_connection import IPConnection


class tf_base(baselogger.BaseLogger):
    """Base class for all tinkerforge sensors
    """
    def __init__(self, db, threadID, name, table, settings):
        baselogger.BaseLogger.__init__(self, db, threadID, name, table,
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

    def get_timestamp(self):
        return datetime.datetime.now()
