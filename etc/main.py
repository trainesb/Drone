from mpu6050 import MPU6050
from datetime import datetime, timedelta
import pigpio
from subprocess import call
from time import sleep

# Start `pigpiod` daemon for the temp/hum sensor
try:
    call(['sudo', 'pigpiod'])
except Exception as err:
    print('Warning: ', err)

pi = pigpio.pi()

mpu = MPU6050()

FrontRight = 20
BackRight = 8
FrontLeft = 19
BackLeft = 24

total_angle_x = 0
total_angle_y = 0
desired_angle_y = 0
desired_angle_x = 0

pid_p_y = 0
pid_i_y = 0
pid_d_y = 0

pid_p_x = 0
pid_i_x = 0
pid_d_x = 0

kp = 5
ki = 0.005
kd = 1

throttle=1375
PID_y = 0
PID_x = 0
pwmBackLeft = 0
pwmBackRight = 0
pwmFrontLeft = 0
pwmFrontRight = 0

previous_error_y = 0
previous_error_x = 0

time = datetime.now()

pi.set_servo_pulsewidth(FrontRight, 1000)
pi.set_servo_pulsewidth(FrontLeft, 1000)
pi.set_servo_pulsewidth(BackRight, 1000)
pi.set_servo_pulsewidth(BackLeft, 1000)

sleep(5)

try:
    while True:
        timePrev = time
        time = datetime.now()
        elapsedTime = (time - timePrev).total_seconds()

        gyro = mpu.getRotation()
        total_angle_x = 0.98 * (total_angle_x + gyro['gyro_xout'] * elapsedTime) + 0.02 * gyro['accel_angle_x']
        total_angle_y = 0.98 * (total_angle_y + gyro['gyro_yout'] * elapsedTime) + 0.02 * gyro['accel_angle_y']


        error_y = total_angle_y - desired_angle_y
        error_x = total_angle_x - desired_angle_x

        print('Error: ', error)
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
        if pwmBackLeft > 2000:
            pwmBackLeft = 2000

        if pwmBackRight < 1000:
            pwmBackRight = 1000
        if pwmBackRight > 2000:
            pwmBackRight = 2000

        if pwmFrontLeft < 1000:
            pwmFrontLeft = 1000
        if pwmFrontLeft > 2000:
            pwmFrontLeft = 2000

        if pwmFrontRight < 1000:
            pwmFrontRight = 1000
        if pwmFrontRight > 2000:
            pwmFrontRight = 2000

        pi.set_servo_pulsewidth(FrontRight, pwmFrontRight)
        pi.set_servo_pulsewidth(FrontLeft, pwmFrontLeft)
        pi.set_servo_pulsewidth(BackRight, pwmBackRight)
        pi.set_servo_pulsewidth(BackLeft, pwmBackLeft)

        previous_error_y = error_y
        previous_error_x = error_x
except KeyboardInterrupt:
    pi.set_servo_pulsewidth(FrontRight, 0)
    pi.set_servo_pulsewidth(FrontLeft, 0)
    pi.set_servo_pulsewidth(BackRight, 0)
    pi.set_servo_pulsewidth(BackLeft, 0)
