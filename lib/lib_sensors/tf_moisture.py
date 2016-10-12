# *-* coding: utf-8 *-*
import sys
import lib_sensors.tf_base as tf_base
from tinkerforge.bricklet_moisture import Moisture
import sqlalchemy as sa
import logging


class tf_moisture(tf_base.tf_base):
    def _create_device_obj(self):
        # Create device object
        self.obj = Moisture(self.uid, self.ipcon)

    def _get_data(self):
        try:
            # unit: relative humidity (RHL) [%]
            moisture = self.obj.get_moisture_value() / 10.0
        except:
            logging.error('There was an error retrieving the moisture.')
            e = sys.exc_info()[0]
            logging.error('Exception: {0}'.format(e))
            return
        time_now = self.get_timestamp()
        logging.debug(
            'moisture: {0} {1} (logger id: {2}'.format(moisture, time_now, self.logger_id))
        ins = self.table(value=moisture,
                         logger_id=self.logger_id,
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
            logger_id = sa.Column(sa.types.Integer)
            value = sa.Column(sa.types.String)
            datetime = sa.Column(sa.types.DateTime)
        return tf_moisture_table
