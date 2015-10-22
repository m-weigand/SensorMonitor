"""
Arduino water table logger
"""
import serial
import baselogger
import logging
import sqlalchemy as sa


class arduino_wt(baselogger.BaseLogger):
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
        self.device = '/dev/ttyUSB0'

        # http://stackoverflow.com/questions/23025021/how-would-i-add-the-timezone-to-a-datetime-datetime-object#23025048
        self.ser = serial.Serial(self.device, 9600)

    def _get_data(self):
        """Query the logger and store a measurement in the table. No return
        values.
        """
        dataline = self.ser.readline().strip()
        last_delim = dataline.rfind('%')
        second_to_last_delim = dataline.rfind('%', 0, last_delim) + 1
        data = dataline[second_to_last_delim: last_delim].split(',')
        temperature = data[0]
        water_table = data[1]
        time_now = self.get_timestamp()

        logging.debug(
            'ar_wt: {0}, datetime: {1}, logger_id: {2}'.format(
                data,
                time_now,
                self.logger_id))

        ins = self.table(value=water_table,
                         value1=temperature,
                         logger_id=self.logger_id,
                         datetime=time_now)

        self.session.add(ins)
        self.session.commit()

    @staticmethod
    def get_table(base, engine):
        """Create the sensor specific table if it does not exist yet
        """
        class ar_wt_table(base):
            __tablename__ = 'ar_wt'
            __table_args__ = {"useexisting": True}

            id = sa.Column(sa.types.Integer, primary_key=True)
            logger_id = sa.Column(sa.types.Integer)
            value = sa.Column(sa.types.String)
            value1 = sa.Column(sa.types.String)
            datetime = sa.Column(sa.types.DateTime)
        return ar_wt_table

    @staticmethod
    def plot(cls, db, logger_item):
        return 'Plot not implented for ar_wt'
