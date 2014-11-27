from tinkerforge.bricklet_temperature import Temperature
import tf_base
import sqlalchemy as sa
import datetime


class sensor(tf_base.tf_base):
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
            datetime.datetime.now().strftime(r'%Y%m%d_%H%M:%S'),
            self.uid, self.name)
        ins = self.table(value=temperature,
                         name=self.name,
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
            name = sa.Column(sa.types.String)
            value = sa.Column(sa.types.String)
            datetime = sa.Column(sa.types.DateTime)
        return tf_temp_table
