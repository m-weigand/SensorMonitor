import sys
import lib_sensors.tf_base as tf_base
from tinkerforge.bricklet_ambient_light import AmbientLight
import sqlalchemy as sa
import logging


class tf_light(tf_base.tf_base):
    @staticmethod
    def description():
        description = """Tinkerforge ambient light sensor
        (setting example: 127.0.0.1:4223:meK)"""
        return description

    def _create_device_obj(self):
        # Create device object
        logging.info('Creating TF connection to AmbientLight:')
        logging.info('  UID: {0} HOST: {1} PORT: {2}'.format(
            self.uid, self.host, self.port))
        self.al = AmbientLight(self.uid, self.ipcon)

    def _get_data(self):
        """
        Write illuminance to log file
        """
        # Get current illuminance (unit is Lux/10)
        try:
            illuminance = self.al.get_illuminance() / 10.0
        except:
            logging.error('There was an error retrieving the illuminance.')
            e = sys.exc_info()[0]
            logging.error('Exception: {0}'.format(e))
            return

        time_now = self.get_timestamp()

        logging.debug(
            'illuminance: {0}, datetime: {1}, logger_id: {2}'.format(
                illuminance,
                time_now,
                self.logger_id))
        ins = self.table(value=illuminance,
                         logger_id=self.logger_id,
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
            # refers to the row id in the sensors-table
            logger_id = sa.Column(sa.types.Integer)
            value = sa.Column(sa.types.String)
            datetime = sa.Column(sa.types.DateTime)
        return tf_light_table
