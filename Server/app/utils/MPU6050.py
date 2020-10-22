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

    def get_z_rotation(self, x, y, z):
        radians = math.atan2(z, self.dist(x, y))
        return math.degrees(radians)

    def getGyro(self):
        x = self.read_word_2c(0x43)/131.0
        y = self.read_word_2c(0x45)/131.0
        z = self.read_word_2c(0x47)/131.0
        return {'x': x, 'y': y, 'z': z}

    def getAccel(self):
        x = self.read_word_2c(0x3b) / 16384.0
        y = self.read_word_2c(0x3d) / 16384.0
        z = self.read_word_2c(0x3f) / 16384.0
        return {'x': x, 'y': y, 'z': z}

    def getRotation(self):
        accel = self.getAccel()
        roll = self.get_x_rotation(accel['x'], accel['y'], accel['z'])
        pitch = self.get_y_rotation(accel['x'], accel['y'], accel['z'])
        yaw = self.get_z_rotation(accel['x'], accel['y'], accel['z'])
        return {'roll': roll, 'pitch': pitch, 'yaw': yaw}
