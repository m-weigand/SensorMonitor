"""
Implement a one-wire logger module to read out temperature sensors attached to
the computer, and exposed via /sys/bus/w1
"""
import baselogger
import logging
import sqlalchemy as sa


class w1_temp(baselogger.BaseLogger):
    def __init__(self, db, threadID, name, logger_id, table, settings):
        """

        Parameters
        ----------
        settings: Identifier of the 1-wire sensor to read out

        """
        baselogger.BaseLogger.__init__(self,
                                       db,
                                       threadID,
                                       name,
                                       logger_id,
                                       table,
                                       settings)
        basepath = '/sys/bus/w1/devices/'
        self.filename = basepath + settings + '/w1_slave'

    def _get_data(self):
        """Query the logger and store a measurement in the table. No return
        values.
        """
        with open(self.filename, 'r') as fid:
            # we are not interested in the first line
            fid.readline()
            # second line
            line = fid.readline().strip()
            # the temperature is written in milli-degrees in the form
            # t=23456, but preceeded by a large HEX data dump in the form
            # 2c 00 4b 46 ff ff 0e 10 17 t=21875
            index = line.find('t=') + 2
            temperature = int(line[index:index + 6]) / 1e3
        time_now = self.get_timestamp()

        logging.debug(
            'w1_temp: {0}, datetime: {1}, logger_id: {2}'.format(
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
        class w1_temp_table(base):
            __tablename__ = 'w1_temp'
            __table_args__ = {"useexisting": True}

            id = sa.Column(sa.types.Integer, primary_key=True)
            logger_id = sa.Column(sa.types.Integer)
            value = sa.Column(sa.types.String)
            datetime = sa.Column(sa.types.DateTime)
        return w1_temp_table

    @staticmethod
    def plot(cls, db, logger_item):
        return 'Plot not implented for w1_temp'
