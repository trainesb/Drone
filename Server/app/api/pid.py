import pigpio
import threading
import time
from flask import current_app
from app.api import bp
from app import db, mpu, qmc, bmp280
from datetime import datetime
from app.models.Controller import Controller
from app.models.PID import PID

pi = pigpio.pi()
break_thread = False
thread = None

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
    break_thread = True
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

# Start the Drone
@bp.route('/api/start', methods=['GET'])
def startDrone():
    break_thread = False
    thread = threading.Thread(target=PID, kwargs={'app': current_app._get_current_object()})
    thread.start()
    return {'status': True}

def PID(app):
    with app.app_context():
        # Totals
        total_angle_x = 0
        total_angle_y = 0

        # PID Variables
        pid_roll_p = 0
        pid_roll_i = 0
        pid_roll_d = 0

        pid_pitch_p = 0
        pid_pitch_i = 0
        pid_pitch_d = 0

        PID_roll = 0
        PID_pitch = 0

        # Motor PWM
        pwmBackLeft = 0
        pwmBackRight = 0
        pwmFrontLeft = 0
        pwmFrontRight = 0

        # Previous Errors
        previous_error_roll = 0
        previous_error_pitch = 0

        time = datetime.now()
        while True:
            if break_thread: break
            pid = PID.query.first()


            velocity_x = controller.velocity_x
            timePrev = time
            time = datetime.now()
            elapsedTime = (time - timePrev).total_seconds()
            gyro = mpu.getRotation()
            controller.velocity_x += gyro['accel_xout'] * elapsedTime

            throttle = controller.freq

            desired_angle_x = pid.desired_angel_x
            roll_p = pid.roll_p
            roll_i = pid.roll_i
            roll_d = pid.roll_d
            total_angle_x = 0.98 * (total_angle_x + gyro['gyro_xout'] * elapsedTime) + 0.02 * gyro['accel_angle_x']
            error_x = total_angle_x - desired_angle_x
            pid_roll_p = roll_p * error_x
            if error_x > -3 and error_x < 3:
                pid_roll_i = pid_roll_i + (roll_i * error_x)
            pid_roll_d = roll_d * ((error_x - previous_error_roll) / elapsedTime)
            PID_roll = pid_roll_p + pid_roll_i + pid_roll_d
            if PID_roll < -400:
                PID_roll = 400
            if PID_roll > 400:
                PID_roll = 400


            desired_angle_y = pid.desired_angel_y
            pitch_p = pid.pitch_p
            pitch_i = pid.pitch_i
            pitch_d = pid.pitch_d
            total_angle_y = 0.98 * (total_angle_y + gyro['gyro_yout'] * elapsedTime) + 0.02 * gyro['accel_angle_y']
            error_y = total_angle_y - desired_angle_y
            pid_pitch_p = pitch_p * error_y
            if error_y > -3 and error_y < 3:
                pid_pitch_i = pid_pitch_i + (pitch_i * error_y)
            pid_pitch_d = pitch_d * ((error_y - previous_error_pitch) / elapsedTime)
            PID_pitch = pid_pitch_p + pid_pitch_i + pid_pitch_d
            if PID_pitch < -400:
                PID_pitch = 400
            if PID_pitch > 400:
                PID_pitch = 400



            pwmBackLeft = throttle - PID_pitch + PID_roll
            pwmBackRight = throttle + PID_pitch + PID_roll
            pwmFrontLeft = throttle - PID_pitch - PID_roll
            pwmFrontRight = throttle + PID_pitch - PID_roll

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

            previous_error_pitch = error_y
            previous_error_roll = error_x

            db.session.add(controller)
            db.session.commit()
