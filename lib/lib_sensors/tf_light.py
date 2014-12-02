import tf_base
import datetime
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_moisture import Moisture
import sqlalchemy as sa


class tf_light(tf_base.tf_base):
    def _create_device_obj(self):
        # Create device object
        self.al = AmbientLight(self.uid, self.ipcon)

    def _get_data(self):
        """
        Write illuminance to log file
        """
        # Get current illuminance (unit is Lux/10)
        try:
            illuminance = self.al.get_illuminance() / 10.0
        except:
            print('There was an error retrieving the illuminance.')
            return

        time_now = self.get_timestamp()
        print(
            'Illuminance ', illuminance,
            datetime.datetime.now().strftime(r'%Y%m%d_%H%M:%S'))
        ins = self.table(value=illuminance,
                         name=self.name,
                         datetime=time_now)

        self.session.add(ins)
        self.session.commit()

    @staticmethod
    def get_table(base, engine):
        """Create the sensor specific table if it does not exist yet
        """
        class tf_light_table(base):
            __tablename__ = 'tf_light'
            __table_args__ = {"useexisting": True}

            id = sa.Column(sa.types.Integer, primary_key=True)
            # name should somehow be related to name in sensors
            name = sa.Column(sa.types.String)
            value = sa.Column(sa.types.String)
            datetime = sa.Column(sa.types.DateTime)
        return tf_light_table


class tf_moisture(tf_base.tf_base):
    def _create_device_obj(self):
        # Create device object
        self.obj = Moisture(self.uid, self.ipcon)

    def _get_data(self):
        try:
            moisture = self.obj.get_moisture_value()
        except:
            print('There was an error retrieving the moisture.')
            return
        time_now = self.get_timestamp()
        print(
            'Moisture ', moisture,
            datetime.datetime.now().strftime(r'%Y%m%d_%H%M:%S'))
        ins = self.table(value=moisture,
                         name=self.name,
                         datetime=time_now)

        self.session.add(ins)
        self.session.commit()

    @staticmethod
    def get_table(base, engine):
        """Create the sensor specific table if it does not exist yet
        """
        class tf_moisture_table(base):
            __tablename__ = 'tf_moisture'
            __table_args__ = {"useexisting": True}

            id = sa.Column(sa.types.Integer, primary_key=True)
            # name should somehow be related to name in sensors
            name = sa.Column(sa.types.String)
            value = sa.Column(sa.types.String)
            datetime = sa.Column(sa.types.DateTime)
        return tf_moisture_table
