import sys
from tinkerforge.bricklet_temperature import Temperature
import tf_base
import sqlalchemy as sa
import logging


class sensor(tf_base.tf_base):
    @staticmethod
    def description():
        description = """Tinkerforge temperature sensor"""
        return description

    def _create_device_obj(self):
        logging.info('Creating TF connection to Temperature:')
        logging.info('  UID: {0} HOST: {1} PORT: {2}'.format(
            self.uid, self.host, self.port))
        # Create device object
        self.temp = Temperature(self.uid, self.ipcon)

    def _get_data(self):
        """
        Write illuminance to log file
        """
        try:
            temperature = self.temp.get_temperature() / 100.0
        except:
            logging.error('There was an error retrieving the temperature.')
            e = sys.exc_info()[0]
            logging.error('Exception: {0}'.format(e))
            return
        time_now = self.get_timestamp()
        logging.debug(
            'temperature: {0} degrees, datetime: {1}, logger_id: {2}'.format(
                temperature,
                time_now,
                self.logger_id))
        ins = self.table(value=temperature,
                         logger_id=self.logger_id,
                         datetime=time_now)

        self.session.add(ins)
        self.session.commit()

    @staticmethod
    def get_table(base, engine):
        """Create the sensor specific table if it does not exist yet
        """
        class tf_temp_table(base):
            __tablename__ = 'tf_temp'
            __table_args__ = {"useexisting": True}
            autoload = True

            id = sa.Column(sa.types.Integer, primary_key=True)
            # name should somehow be related to name in sensors
            logger_id = sa.Column(sa.types.Integer)
            value = sa.Column(sa.types.String)
            datetime = sa.Column(sa.types.DateTime)
        return tf_temp_table
