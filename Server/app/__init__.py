import board
import busio
import adafruit_bmp280
from subprocess import call
from flask import Flask
from flask_cors import CORS
from config import Config
from app.utils.MPU6050 import MPU6050
from app.utils.QMC5883L import QMC5883L
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Start `pigpiod` daemon for the temp/hum sensor
try:
    call(['sudo', 'pigpiod'])
except Exception as err:
    print('Warning: ', err)

mpu = MPU6050()
qmc = QMC5883L()

i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
bmp280.sea_level_pressure = 1013.25

db = SQLAlchemy()

migrate = Migrate(compare_type=True)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    from app.models import bp as models_bp
    app.register_blueprint(models_bp)

    return app
