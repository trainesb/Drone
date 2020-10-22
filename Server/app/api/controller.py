from app.api import bp
from app import db, mpu, qmc, bmp280
from datetime import datetime
from app.models.Controller import Controller
from app.models.PID import PID

# Get PWM
@bp.route('/api/pwm', methods=['GET'])
def getPWM():
    controller = Controller.query.first()
    return {'fr': controller.pwmFrontRight, 'fl': controller.pwmFrontLeft, 'br': controller.pwmBackRight, 'bl': controller.pwmBackLeft}

# Get Controller Velocity X
@bp.route('/api/speed', methods=['GET'])
def getSpeed():
    controller = Controller.query.first()
    return {'velocity_x': controller.velocity_x}

# Get Controller Desired Angles
@bp.route('/api/desired/angles', methods=['GET'])
def getDesiredAngles():
    pid = PID.query.first()
    return {'desired_angel_x': pid.desired_angel_x, 'desired_angel_y': pid.desired_angel_y}

# Set Controler Desired Angle
@bp.route('/api/desired/angle/<string:name>/<float:angle>', methods=['GET'])
def setDesiredAngle(name, angle):
    pid = PID.query.first()
    if name == 'x': pid.desired_angel_x = angle
    elif name == 'y': pid.desired_angel_y = angle
    return {'status': True}

# Get PID
@bp.route('/api/PID/<string:name>/<string:var>', methods=['GET'])
def getPID(name, var):
    pid = PID.query.first()
    if name == 'roll':
        if var == 'p': return {'roll_p': pid.roll_p}
        elif var == 'i': return {'roll_i': pid.roll_i}
        elif var == 'd': return {'roll_d': pid.roll_d}
    elif name == 'pitch':
        if var == 'p': return {'pitch_p': pid.pitch_p}
        elif var == 'i': return {'pitch_i': pid.pitch_i}
        elif var == 'd': return {'pitch_d': pid.pitch_d}
    return {'status': False}


# Set Controller PID
@bp.route('/api/PID/<string:name>/<string:var>/<float:val>', methods=['GET'])
def setKP(name, var, val):
    pid = PID.query.first()
    if name == 'roll':
        if var == 'p': pid.roll_p = val
        elif var == 'i': pid.roll_i = val
        elif var == 'd': pid.roll_d = val
    elif name == 'pitch':
        if var == 'p': pid.pitch_p = val
        elif var == 'i': pid.pitch_i = val
        elif var == 'd': pid.pitch_d = val
    db.session.add(pid)
    db.session.commit()
    return {'status': True}

# Get Throttle Freq
@bp.route('/api/throttle', methods=['GET'])
def getThrottle():
    controller = Controller.query.first()
    return {'throttle': controller.freq}

# Set Throttle Freq
@bp.route('/api/throttle/<int:freq>', methods=['GET'])
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
