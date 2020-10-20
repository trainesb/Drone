import pigpio
import threading
import time
from flask import current_app
from app.api import bp
from app import db, mpu, qmc, bmp280
from datetime import datetime
from app.models.Controller import Controller

pi = pigpio.pi()

# Get Gyro X
@bp.route('/api/turn', methods=['GET'])
def getTurn():
    return {'turn': mpu.getRotation()['gyro_xout']}

# Get Accel Z
@bp.route('/api/vario', methods=['GET'])
def getVario():
    return {'vario': mpu.getRotation()['accel_zout']}

# Get Controller Velocity X
@bp.route('/api/speed', methods=['GET'])
def getSpeed():
    controller = Controller.query.first()
    return {'velocity_x': controller.velocity_x}

# Get Controller Desired Angles
@bp.route('/api/desired/angles', methods=['GET'])
def getDesiredAngles():
    controller = Controller.query.first()
    return {'desired_angel_x': controller.desired_angel_x, 'desired_angel_y': controller.desired_angel_y}

# Set Controler Desired Angle
@bp.route('/api/desired/angle/<string:name>/<float:angle>', methods=['GET'])
def setDesiredAngle(name, angle):
    controller = Controller.query.first()
    if name == 'x': controller.desired_angel_x = angle
    elif name == 'y': controller.desired_angel_y = angle
    return {'status': True}

# Get Controller PID
@bp.route('/api/PID', methods=['GET'])
def getPID():
    controller = Controller.query.first()
    return {'kp': controller.kp, 'ki': controller.ki, 'kd': controller.kd}

# Set Controller PID
@bp.route('/api/PID/<string:pid>/<float:val>', methods=['GET'])
def setPID(pid, val):
    controller = Controller.query.first()
    if pid == 'kp':
        controller.kp = val
    elif pid == 'ki':
        controller.ki = val
    elif pid == 'kd':
        controller.kd = val
    db.session.add(controller)
    db.session.commit()
    return {'status': True}

# Get Throttle Freq
@bp.route('/api/throttle', methods=['GET'])
def getThrottle():
    controller = Controller.query.first()
    return {'throttle': controller.freq}

# Set Throttle Freq
@bp.route('/api/throttle/<float:freq>', methods=['GET'])
def setThrottle(freq):
    controller = Controller.query.first()
    controller.freq = freq
    db.session.add(controller)
    db.session.commit()
    return {'status': True}

# Get BMP280 data
@bp.route('/api/BMP280', methods=['GET'])
def getBMP280():
    return { 'temp': bmp280.temperature, 'pressure': bmp280.pressure, 'altitude': bmp280.altitude }

# Get Heading
@bp.route('/api/heading', methods=['GET'])
def getHeading():
    return {'heading': qmc.get_bearing()}

# Get MPU data
@bp.route('/api/mpu', methods=['GET'])
def getMPU():
    return mpu.getRotation()

# Prime the Drone
@bp.route('/api/prime', methods=['GET'])
def primeDrone():
    controller = Controller.query.first()
    pi.set_servo_pulsewidth(controller.front_right, 1000)
    pi.set_servo_pulsewidth(controller.front_left, 1000)
    pi.set_servo_pulsewidth(controller.back_right, 1000)
    pi.set_servo_pulsewidth(controller.back_left, 1000)
    time.sleep(1)
    return {'status': True}

# Stop the Drone
@bp.route('/api/stop', methods=['GET'])
def stopDrone():
    thread.join()
    controller = Controller.query.first()
    controller.freq = 1000
    pi.set_servo_pulsewidth(controller.front_right, 0)
    pi.set_servo_pulsewidth(controller.front_left, 0)
    pi.set_servo_pulsewidth(controller.back_right, 0)
    pi.set_servo_pulsewidth(controller.back_left, 0)
    db.session.add(controller)
    db.session.commit()
    return {'status': True}

thread = None
# Start the Drone
@bp.route('/api/start', methods=['GET'])
def startDrone():
    thread = threading.Thread(target=PID, kwargs={'app': current_app._get_current_object()})
    thread.start()
    return {'status': True}

# PID
def PID(app):
    with app.app_context():
        total_angle_x = 0
        total_angle_y = 0

        pid_p_y = 0
        pid_i_y = 0
        pid_d_y = 0

        pid_p_x = 0
        pid_i_x = 0
        pid_d_x = 0

        PID_y = 0
        PID_x = 0
        pwmBackLeft = 0
        pwmBackRight = 0
        pwmFrontLeft = 0
        pwmFrontRight = 0

        previous_error_y = 0
        previous_error_x = 0

        time = datetime.now()
        while True:
            controller = Controller.query.first()
            desired_angle_y = controller.desired_angel_y
            desired_angle_x = controller.desired_angel_x
            velocity_x = controller.velocity_x
            kp = controller.kp
            ki = controller.ki
            kd = controller.kd
            throttle = controller.freq

            timePrev = time
            time = datetime.now()
            elapsedTime = (time - timePrev).total_seconds()

            gyro = mpu.getRotation()
            print('Velocity X: ', controller.velocity_x)
            controller.velocity_x += gyro['accel_xout'] * elapsedTime

            total_angle_x = 0.98 * (total_angle_x + gyro['gyro_xout'] * elapsedTime) + 0.02 * gyro['accel_angle_x']
            total_angle_y = 0.98 * (total_angle_y + gyro['gyro_yout'] * elapsedTime) + 0.02 * gyro['accel_angle_y']

            error_y = total_angle_y - desired_angle_y
            error_x = total_angle_x - desired_angle_x

            pid_p_y = kp * error_y
            pid_p_x = kp * error_x
            if error_y > -3 and error_y < 3:
                pid_i_y = pid_i_y + (ki * error_y)
            if error_x > -3 and error_x < 3:
                pid_i_x = pid_i_x + (ki * error_x)

            pid_d_y = kd * ((error_y - previous_error_y) / elapsedTime)
            PID_y = pid_p_y + pid_i_y + pid_d_y

            pid_d_x = kd * ((error_x - previous_error_x) / elapsedTime)
            PID_x = pid_p_x + pid_i_x + pid_d_x

            if PID_y < -1000:
                PID_y = 1000
            if PID_y > 1000:
                PID_y = 1000

            if PID_x < -1000:
                PID_x = 1000
            if PID_x > 1000:
                PID_x = 1000

            print("PID: ", PID)

            pwmBackLeft = throttle - PID_y + PID_x
            pwmBackRight = throttle + PID_y + PID_x
            pwmFrontLeft = throttle - PID_y - PID_x
            pwmFrontRight = throttle + PID_y - PID_x

            if pwmBackLeft < 1000:
                pwmBackLeft = 1000
            if pwmBackLeft > 2500:
                pwmBackLeft = 2500

            if pwmBackRight < 1000:
                pwmBackRight = 1000
            if pwmBackRight > 2500:
                pwmBackRight = 2500

            if pwmFrontLeft < 1000:
                pwmFrontLeft = 1000
            if pwmFrontLeft > 2500:
                pwmFrontLeft = 2500

            if pwmFrontRight < 1000:
                pwmFrontRight = 1000
            if pwmFrontRight > 2500:
                pwmFrontRight = 2500

            pi.set_servo_pulsewidth(controller.front_right, pwmFrontRight)
            pi.set_servo_pulsewidth(controller.front_left, pwmFrontLeft)
            pi.set_servo_pulsewidth(controller.back_right, pwmBackRight)
            pi.set_servo_pulsewidth(controller.back_left, pwmBackLeft)

            previous_error_y = error_y
            previous_error_x = error_x

            db.session.add(controller)
            db.session.commit()
