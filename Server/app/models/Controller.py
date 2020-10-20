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

    kp = db.Column(db.Float)
    ki = db.Column(db.Float)
    kd = db.Column(db.Float)

    desired_angel_y = db.Column(db.Float)
    desired_angel_x = db.Column(db.Float)

    velocity_x = db.Column(db.Float)


    def __init__ (self):
        self.max_freq = 2500
        self.freq = 1000

        self.front_right = 20
        self.back_right = 8
        self.front_left = 19
        self.back_left = 24

        self.kp = 5
        self.ki = 0.005
        self.kd = 1

        self.desired_angel_y = 0
        self.desired_angel_x = 0

        self.velocity_x = 0.0

    def __repr__(self):
        return '<Controller ID:{} MaxFreq:{} Freq:{} FR:{} FL:{} BR:{} BL:{} kp:{} ki:{} kd:{}>'.format(self.id, self.max_freq, self.freq, self.front_right, self.front_left, self.back_right, self.back_left, self.kp, self.ki, self.kd)

    def _toDict(self):
        return {
            'id': self.id,
            'max_freq': self.max_freq,
            'freq': self.freq,
            'front_right': self.front_right,
            'front_left': self.front_left,
            'back_right': self.back_right,
            'back_left': self.back_left,
            'kp': self.kp,
            'ki': self.ki,
            'kd': self.kd,
            'desired_angel_y': self.desired_angel_y,
            'desired_angel_x': self.desired_angel_x,
            'velocity_x': self.velocity_x
        }
