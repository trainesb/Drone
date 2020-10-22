from app import db

class Controller(db.Model):
    __tablename__ = 'controller'

    id = db.Column(db.Integer, primary_key=True)
    max_freq = db.Column(db.Integer)
    freq = db.Column(db.Integer)

    # Motor GPIO
    front_right = db.Column(db.Integer)
    front_left = db.Column(db.Integer)
    back_right = db.Column(db.Integer)
    back_left = db.Column(db.Integer)

    velocity_x = db.Column(db.Float)
    velocity_z = db.Column(db.Float)

    pwmBackLeft = db.Column(db.Float)
    pwmBackRight = db.Column(db.Float)
    pwmFrontLeft = db.Column(db.Float)
    pwmFrontRight = db.Column(db.Float)


    def __init__ (self):
        self.max_freq = 2500
        self.freq = 1000

        self.front_right = 20
        self.back_right = 8
        self.front_left = 19
        self.back_left = 24

        self.velocity_x = 0.0
        self.velocity_z = 0.0

        self.pwmBackLeft = 0.0
        self.pwmBackRight = 0.0
        self.pwmFrontLeft = 0.0
        self.pwmFrontRight = 0.0

    def __repr__(self):
        return '<Controller ID:{} MaxFreq:{} Freq:{} FR:{} FL:{} BR:{} BL:{}>'.format(self.id, self.max_freq, self.freq, self.front_right, self.front_left, self.back_right, self.back_left)

    def _toDict(self):
        return {
            'id': self.id,
            'max_freq': self.max_freq,
            'freq': self.freq,
            'front_right': self.front_right,
            'front_left': self.front_left,
            'back_right': self.back_right,
            'back_left': self.back_left,
            'velocity_x': self.velocity_x
        }
