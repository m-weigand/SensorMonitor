#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
The program reacts to SIGTERM (15) and shuts itself down
"""
import signal
import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
import threading
import lib_sensors.sensors as SL
sensor_types = SL.available_loggers


class LoggerManager(threading.Thread):
    """Manage the logger threads, and query the sensors table in regular
       intervals. Then check the existing threads a) for correct settings b) for
       existance. Stop and start any thread with wrong settings or non-existens
       names
    """
    def __init__(self, settings):
        threading.Thread.__init__(self)
        self.settings = settings
        self.create_database()
        self.counter = 0
        self.loggers = {}
        self.tables = {}
        self.lock = threading.Lock()  # use to set the exit flag
        self.exitFlag = False

    def create_database(self):
        """Create/open the database including the sensors table
        """
        if 'database' in self.settings:
            filename = self.settings['database']
        else:
            filename = 'sensors.db'
        engine = sa.create_engine('sqlite:///{0}'.format(filename), echo=False)
        Base = declarative_base(bind=engine)

        class sensors(Base):
            __tablename__ = 'sensors'
            # __table_args__ = {'autoload': True}

            id = sa.Column(sa.types.Integer, primary_key=True)
            type = sa.Column(sa.types.String)
            name = sa.Column(sa.types.String)
            log = sa.Column(sa.types.Boolean)
            interval = sa.Column(sa.types.Integer)
            description = sa.Column(sa.types.String)
            settings = sa.Column(sa.types.String)

        # create the table
        Base.metadata.create_all(engine)

        # create a scoped session for use with the Threads
        Session = sqlalchemy.orm.scoped_session(sessionmaker(bind=engine))

        db = {'engine': engine,
              'session': Session,
              'base': Base,
              'sensors': sensors
              }

        self.db = db

    def delete_database(self):
        if(os.path.isfile('sensors.db')):
            os.unlink('sensors.db')

    def _get_exitFlag(self):
        with self.lock:
            exitFlag = self.exitFlag
        return exitFlag

    def run(self):
        while not self._get_exitFlag():
            self.check_loggers()
            time.sleep(self.settings['interval'])

    def signal_term_handler(self, signal, frame):
        for ltype in self.loggers.keys():
            for logger in self.loggers[ltype]:
                with logger.lock:
                    logger.exitFlag = True
        # now quit this logger manager thread
        with self.lock:
            self.exitFlag = True

    def check_loggers(self):
        """
        - query sensors table to get settings
        - then loop over the sensors and create corresponding DateLogger objects
        - store in list
        """

        # get sensor settings
        sensor_list = self.db['session'].query(self.db['sensors'])
        for item in sensor_list:
            # is this logger active?
            if not item.log:
                # check if logger is running and stop
                continue
            else:
                # print 'name', item.name
                is_in_dict = item.type in self.loggers
                # print 'is_in_dict', is_in_dict

                not_created_yet = False
                if is_in_dict:
                    started_logger = None
                    for logger in self.loggers[item.type]:
                        if logger.name == item.name:
                            started_logger = logger
                            not_created_yet = False
                            break
                    if started_logger is None:
                        not_created_yet = True
                else:
                    self.loggers[item.type] = []
                    self.tables[item.type] = sensor_types[
                        item.type].get_table(self.db['base'], self.db['engine'])
                    not_created_yet = True

                if not_created_yet:
                    # table_date_logger = DateLogger.get_table(
                    #    self.db['base'],
                    #    self.db['engine'])
                    table_logger = self.tables[item.type]
                    new_logger = sensor_types[item.type](
                        self.db, self.counter,
                        item.name, table_logger,
                        item.settings)

                    # set settings
                    new_logger.interval = item.interval
                    self.loggers[item.type].append(new_logger)
                    self.counter += 1
                    new_logger.start()

    def start_loggers(self):
        for logger in self.loggers:
            logger.start()
        print 'threads started'
        print threading.active_count()

    def wait(self):
        for logger in self.loggers:
            logger.join()


def main():
    settings = {'interval': 10
                }
    logger_manager = LoggerManager(settings)

    # we want to catch sigterm and stop the processes
    signal.signal(signal.SIGTERM, logger_manager.signal_term_handler)

    # don't start as a thread, otherwise we cannot handle signals properly
    logger_manager.run()
    # logger_manager.join()


if __name__ == '__main__':
    main()
    # date_setup = DateSetup(db)
    # date_setup.start_loggers()
    # date_setup.wait()

    # # from here on :TESTS:
    # date_logger._add_test_sensors()

    """
    print 'query'
    # query = db['session'].query(date_setup.loggers[0].date_time).all()
    query = 1
    print query
    for item in query:
        print item.value
    # # test end

    print 'query sensors'
    query = db['session'].query(db['sensors']).all()
    for item in query:
        print item.name, item.interval, item.log
    """
