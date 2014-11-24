import baselogger
import datetime
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_temperature import Temperature
from tinkerforge.bricklet_moisture import Moisture
import sqlalchemy as sa


class tf_base(baselogger.BaseLogger):
    """Base class for all tinkerforge sensors
    """
    def __init__(self, db, threadID, name, table, settings):
        baselogger.BaseLogger.__init__(self, db, threadID, name, table,
                                       settings)

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


class tf_light(tf_base):
    def _create_device_obj(self):
        # Create device object
        self.al = AmbientLight(self.uid, self.ipcon)

    def _get_data(self):
        """
        Write illuminance to log file
        """
        # Get current illuminance (unit is Lux/10)
        illuminance = self.al.get_illuminance() / 10.0
        time_now = self.get_timestamp()
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
        class tf_light_table(base):
            __tablename__ = 'tf_light'

            id = sa.Column(sa.types.Integer, primary_key=True)
            # name should somehow be related to name in sensors
            name = sa.Column(sa.types.String)
            value = sa.Column(sa.types.String)
            datetime = sa.Column(sa.types.DateTime)
        return tf_light_table


class tf_temp(tf_base):
    def _create_device_obj(self):
        # Create device object
        self.temp = Temperature(self.uid, self.ipcon)

    def _get_data(self):
        """
        Write illuminance to log file
        """
        temperature = self.temp.get_temperature() / 100.0
        time_now = self.get_timestamp()
        print(
            'Temperature ', temperature,
            datetime.datetime.now().strftime(r'%Y%m%d_%H%M:%S'))
        ins = self.table(value=temperature,
                         datetime=time_now)

        self.session.add(ins)
        self.session.commit()

    @staticmethod
    def get_table(base, engine):
        """Create the sensor specific table if it does not exist yet
        """
        class tf_temp_table(base):
            __tablename__ = 'tf_temp'

            id = sa.Column(sa.types.Integer, primary_key=True)
            # name should somehow be related to name in sensors
            name = sa.Column(sa.types.String)
            value = sa.Column(sa.types.String)
            datetime = sa.Column(sa.types.DateTime)
        return tf_temp_table


class tf_moisture(tf_base):
    def _create_device_obj(self):
        # Create device object
        self.obj = Moisture(self.uid, self.ipcon)

    def _get_data(self):
        moisture = self.obj.get_moisture_value()
        time_now = self.get_timestamp()
        print(
            'Moisture ', moisture,
            datetime.datetime.now().strftime(r'%Y%m%d_%H%M:%S'))
        ins = self.table(value=moisture,
                         datetime=time_now)

        self.session.add(ins)
        self.session.commit()

    @staticmethod
    def get_table(base, engine):
        """Create the sensor specific table if it does not exist yet
        """
        class tf_moisture_table(base):
            __tablename__ = 'tf_moisture'

            id = sa.Column(sa.types.Integer, primary_key=True)
            # name should somehow be related to name in sensors
            name = sa.Column(sa.types.String)
            value = sa.Column(sa.types.String)
            datetime = sa.Column(sa.types.DateTime)
        return tf_moisture_table
