from app.api import bp
from app import mpu

# Get Gyro (x, y, z)
@bp.route('/api/MPU/gyro', methods=['GET'])
def getGyro():
    return mpu.getGyro()

# Get Acelleration (x, y, z)
@bp.route('/api/MPU/accel', methods=['GET'])
def getAccel():
    return mpu.getAccel()

# Get Pitch, Roll, and Yaw
@bp.route('/api/MPU/rotation', methods=['GET'])
def getRotation():
    return mpu.getRotation()
