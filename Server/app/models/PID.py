from app import db

class PID(db.Model):
    __tablename__ = 'pid'

    id = db.Column(db.Integer, primary_key=True)

    # Roll (x-axis)
    roll_p = db.Column(db.Float)
    roll_i = db.Column(db.Float)
    roll_d = db.Column(db.Float)

    # Pitch (y-axis)
    pitch_p = db.Column(db.Float)
    pitch_i = db.Column(db.Float)
    pitch_d = db.Column(db.Float)

    # Altitude (z-axis)
    alt_p = db.Column(db.Float)
    alt_i = db.Column(db.Float)
    alt_d = db.Column(db.Float)

    # Air Speed (velocity in x-axis)
    spd_p = db.Column(db.Float)
    spd_i = db.Column(db.Float)
    spd_d = db.Column(db.Float)

    desired_angel_y = db.Column(db.Float)
    desired_angel_x = db.Column(db.Float)
    desired_alt = db.Column(db.Float)
    desired_spd = db.Column(db.Float)


    def __init__ (self):
        self.roll_p = 5
        self.roll_i = 0.005
        self.roll_d = 1

        self.pitch_p = 5
        self.pitch_i = 0.005
        self.pitch_d = 1

        self.alt_p = 5
        self.alt_i = 0.005
        self.alt_d = 1

        self.spd_p = 5
        self.spd_i = 0.005
        self.spd_d = 1

        self.desired_angel_y = 0
        self.desired_angel_x = 0
        self.desired_alt = 0
        self.desired_spd = 0

    def __repr__(self):
        rtrn = '<PID\n'
        rtrn += '\troll_p:{} roll_i:{} roll_d:{}'.format(self.roll_p, self.roll_i, self.roll_d)
        rtrn += '\tpitch_p:{} pitch_i:{} pitch_d:{}'.format(self.pitch_p, self.pitch_i, self.pitch_d)
        rtrn += '\talt_p:{} alt_i:{} alt_d:{}'.format(self.alt_p, self.alt_i, self.alt_d)
        rtrn += '\tspd_p:{} spd_i:{} spd_d:{}'.format(self.spd_p, self.spd_i, self.spd_d)
        rtrn += '\tdesired_angle_y:{} desired_angel_x:{} desired_alt:{} desired_spd:{}\n>'.format(self.desired_angel_y, self.desired_angel_y, self.desired_alt, self.desired_spd)
        return rtrn

    def _toDict(self):
        return {
            'id': self.id,
            'roll_p': self.roll_p,
            'roll_i': self.roll_i,
            'roll_d': self.roll_d,
            'pitch_p': self.pitch_p,
            'pitch_i': self.pitch_i,
            'pitch_d': self.pitch_d,
            'alt_p': self.alt_p,
            'alt_i': self.alt_i,
            'alt_d': self.alt_d,
            'spd_p': self.spd_p,
            'spd_i': self.spd_i,
            'spd_d': self.spd_d,
            'desired_angel_y': self.desired_angel_y,
            'desired_angel_x': self.desired_angel_x,
            'desired_alt': self.desired_alt,
            'desired_spd': self.desired_spd
        }
