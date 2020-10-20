import smbus
import math

class MPU6050:
    # Power management registers
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c

    bus = smbus.SMBus(1)
    address = 0x68

    def __init__(self):
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a, b):
        return math.sqrt((a*a) + (b*b))

    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.dist(y, z))
        return -math.degrees(radians)

    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.dist(x, z))
        return math.degrees(radians)

    def getRotation(self):
        accel_xout = self.read_word_2c(0x3b)
        accel_yout = self.read_word_2c(0x3d)
        accel_zout = self.read_word_2c(0x3f)

        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        accel_angle_x = self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        accel_angle_y = self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)


        gyro_xout = self.read_word_2c(0x43)/131.0
        gyro_yout = self.read_word_2c(0x45)/131.0
        gyro_zout = self.read_word_2c(0x47)/131.0


        return {'accel_angle_x': accel_angle_x, 'accel_angle_y': accel_angle_y, 'gyro_xout': gyro_xout, 'gyro_yout': gyro_yout, 'gyro_zout': gyro_zout}
