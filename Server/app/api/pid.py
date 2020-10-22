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
thread_stopped = False

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
    global break_thread, thread_stopped
    break_thread = True
    while not thread_stopped:
        print('Waitning for thread to stop')
    thread_stopped = False
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
    global break_thread, thread_stopped
    thread_stopped = False
    break_thread = False
    threading.Thread(target=PIDThread, kwargs={'app': current_app._get_current_object()}).start()
    return {'status': True}

def PIDThread(app):
    global break_thread, thread_stopped
    with app.app_context():
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
            controller = Controller.query.first()

            timePrev = time
            time = datetime.now()
            elapsedTime = (time - timePrev).total_seconds()
            rotation = mpu.getRotation()
            accel = mpu.getAccel()
            controller.velocity_x += accel['x'] * elapsedTime


            error_x = rotation['roll'] - pid.desired_angel_x
            pid_roll_p = pid.roll_p * error_x
            if error_x > -3 and error_x < 3:
                pid_roll_i = pid_roll_i + (pid.roll_i * error_x)
            pid_roll_d = pid.roll_d * ((error_x - previous_error_roll) / elapsedTime)
            PID_roll = pid_roll_p + pid_roll_i + pid_roll_d
            if PID_roll < -50: PID_roll = 50
            elif PID_roll > 50: PID_roll = 50


            error_y = rotation['pitch'] - pid.desired_angel_y
            pid_pitch_p = pid.pitch_p * error_y
            if error_y > -3 and error_y < 3:
                pid_pitch_i = pid_pitch_i + (pid.pitch_i * error_y)
            pid_pitch_d = pid.pitch_d * ((error_y - previous_error_pitch) / elapsedTime)
            PID_pitch = pid_pitch_p + pid_pitch_i + pid_pitch_d
            if PID_pitch < -50: PID_pitch = 50
            elif PID_pitch > 50: PID_pitch = 50

            throttle = controller.freq
            pwmBackLeft = throttle - PID_pitch + PID_roll
            pwmBackRight = throttle + PID_pitch + PID_roll
            pwmFrontLeft = throttle - PID_pitch - PID_roll
            pwmFrontRight = throttle + PID_pitch - PID_roll

            if pwmBackLeft < 1000:
                pwmBackLeft = 1000
            if pwmBackLeft > 1500:
                pwmBackLeft = 1500

            if pwmBackRight < 1000:
                pwmBackRight = 1000
            if pwmBackRight > 1500:
                pwmBackRight = 1500

            if pwmFrontLeft < 1000:
                pwmFrontLeft = 1000
            if pwmFrontLeft > 1500:
                pwmFrontLeft = 1500

            if pwmFrontRight < 1000:
                pwmFrontRight = 1000
            if pwmFrontRight > 1500:
                pwmFrontRight = 1500

            #print('\nPWM Front Right: ', pwmFrontRight, ' Front Left: ', pwmFrontLeft)
            #print('\PWM Back Right: ', pwmBackRight, ' Back Left: ', pwmBackLeft, '\n')
            controller.pwmBackLeft = pwmBackLeft
            controller.pwmBackRight = pwmBackRight
            controller.pwmFrontLeft = pwmFrontLeft
            controller.pwmFrontRight = pwmFrontRight


            pi.set_servo_pulsewidth(controller.front_right, pwmFrontRight)
            pi.set_servo_pulsewidth(controller.front_left, pwmFrontLeft)
            pi.set_servo_pulsewidth(controller.back_right, pwmBackRight)
            pi.set_servo_pulsewidth(controller.back_left, pwmBackLeft)

            previous_error_pitch = error_y
            previous_error_roll = error_x

            db.session.add(controller)
            db.session.commit()
    thread_stopped = True
