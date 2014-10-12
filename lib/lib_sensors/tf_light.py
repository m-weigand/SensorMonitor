import BaseLogger
import datetime
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light import AmbientLight
import sqlalchemy as sa


class tf_light(BaseLogger.BaseLogger):
    def __init__(self, db, threadID, name, table):
        BaseLogger.BaseLogger.__init__(self, db, threadID, name, table)

        # tinkerforge settings
        self.host = '127.0.0.1'
        self.port = 4223
        self.light_uid = 'meK'

        self._connect_to_bricklet()

    def _connect_to_bricklet(self):
        # Create IP connection
        self.ipcon = IPConnection()
        # Create device object
        self.al = AmbientLight(self.light_uid, self.ipcon)
        # Connect to brickd
        self.ipcon.connect(self.host, self.port)

    def _disconnect(self):
        self.ipcon.disconnect()

    def _get_data(self):
        """
        Write illuminance to log file
        """
        # Get current illuminance (unit is Lux/10)
        illuminance = self.al.get_illuminance() / 10.0
        time_now = datetime.datetime.now()
        print(
            'Illuminance ', illuminance,
            datetime.datetime.now().strftime(r'%Y%m%d_%H%M:%S'))
        ins = self.table(value=illuminance,
                         datetime=time_now)

        self.session.add(ins)
        self.session.commit()

    @staticmethod
    def get_table(base, engine):
        """Create the sensor specific table if it does not exist yet
        """
        # example, CHANGE:
        class tf_light_table(base):
            __tablename__ = 'tf_light'

            id = sa.Column(sa.types.Integer, primary_key=True)
            # name should somehow be related to name in sensors
            name = sa.Column(sa.types.String)
            value = sa.Column(sa.types.String)
            datetime = sa.Column(sa.types.DateTime)
        return tf_light_table
