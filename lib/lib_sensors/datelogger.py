# -*- coding: utf-8 -*-
import lib_sensors.baselogger as baselogger
import sqlalchemy as sa
import datetime


class DateLogger(baselogger.BaseLogger):
    """Log the datetime
    """
    def _get_data(self):
        reading = datetime.datetime.now()
        reading_str = reading.strftime(r'%Y%m%d_%H%M:%S')
        output = self.name + '   ' + reading_str
        ins = self.table(value=output)

        self.session.add(ins)
        self.session.commit()
        print(output)

    @staticmethod
    def get_table(base, engine):
        """Create the sensor specific table if it does not exist yet
        """

        class date_time(base):
            __tablename__ = 'datetime'

            id = sa.Column(sa.types.Integer, primary_key=True)
            # name should somehow be related to name in sensors
            name = sa.Column(sa.types.String)
            value = sa.Column(sa.types.String)
            time = sa.Column(sa.types.String)
        return date_time
