import threading
# import sqlalchemy as sa
import time
import abc


class BaseLogger(threading.Thread):
    __metaclass__ = abc.ABCMeta
    """This class is the building block of all sensor modules, and should be
    inherited by all sensor classes
    """
    def __init__(self, db, threadID, name, logger_id, table, settings):
        """
        Parameters
        ----------
        db:
        threadID:
        name:
        logger_id: id corresponding to the entry in the sensors table
        table:
        settings:
        """
        threading.Thread.__init__(self)
        self.lock = threading.Lock()  # use to set the exit flag
        self.exitFlag = False
        self.db = db
        self.db['base'].metadata.create_all(self.db['engine'])
        self.table = table
        self.settings = settings

        self.name = name
        self.logger_id = logger_id
        self.threadID = threadID
        self.reading = None

    @staticmethod
    # @abc.abstractmethod
    def description():
        """Return a description string
        """
        return ''

    def initialize(self):
        self.session = self.db['session']()

    def run(self):
        # load settings and create database connection
        self.initialize()
        exitFlag = self._get_exit_flag()

        count = 0  # count seconds
        while(not exitFlag):
            # self.thread_control.qlock.acquire()
            # start_logging = self.thread_control.tf_light.start_logging
            # self.thread_control.qlock.release()
            if not count == 0 and count % self.interval == 0:
                self._get_data()
                count = 0
            else:
                # wait one second before check again
                time.sleep(1)
                count += 1
            exitFlag = self._get_exit_flag()

    def _get_exit_flag(self):
        with self.lock:
            exitFlag = self.exitFlag
        return exitFlag

    @staticmethod
    def create_table(base, engine):
        table = BaseLogger.get_table(base, engine)
        base.metadata.create_all(engine)
        return table
    """
    The following methods must be properly declared by the child class
    """
    @abc.abstractmethod
    def _get_data(self):
        """Query the logger and store a measurement in the table. No return
        values.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_table(base, engine):
        """Create the sensor specific table if it does not exist yet
        """
        # example, CHANGE:
        # class date_time(base):
        #     __tablename__ = 'datetime'
        #     __table_args__ = {"useexisting": True}

        #     id = sa.Column(sa.types.Integer, primary_key=True)
        #     logger_id = sa.Column(sa.types.String)
        #     value = sa.Column(sa.types.String)
        #     datetime = sa.Column(sa.types.DateTime)
        return None

    @staticmethod
    @abc.abstractmethod
    def plot(cls, db, logger_item):
        pass
